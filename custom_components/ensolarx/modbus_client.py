from __future__ import annotations

import asyncio
import logging
import struct
from typing import List, Optional

_LOGGER = logging.getLogger(__name__)


class ModbusError(Exception):
    """Błąd warstwy Modbus."""


class ModbusTcpClient:
    """Minimalny klient Modbus TCP z retry i autoreconnect."""

    def __init__(
        self,
        host: str,
        port: int,
        unit_id: int = 1,
        timeout: float = 3.0,
        retry_attempts: int = 1,
        retry_delay: float = 0.15,
    ) -> None:
        self._host = host
        self._port = port
        self._unit = unit_id
        self._timeout = timeout
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay

        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._tid = 0

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def unit_id(self) -> int:
        return self._unit

    async def connect(self) -> None:
        if self._writer is not None:
            return
        _LOGGER.debug("Connecting Modbus TCP to %s:%s (unit=%s)", self._host, self._port, self._unit)
        self._reader, self._writer = await asyncio.wait_for(
            asyncio.open_connection(self._host, self._port), timeout=self._timeout
        )

    async def close(self) -> None:
        if self._writer is not None:
            self._writer.close()
            try:
                await self._writer.wait_closed()
            except Exception:
                pass
        self._reader = None
        self._writer = None

    async def _send_pdu_once(self, pdu: bytes) -> bytes:
        if self._writer is None or self._reader is None:
            await self.connect()

        self._tid = (self._tid + 1) & 0xFFFF
        length = len(pdu) + 1
        mbap = struct.pack(">HHHB", self._tid, 0, length, self._unit)

        assert self._writer is not None
        assert self._reader is not None

        self._writer.write(mbap + pdu)
        await self._writer.drain()

        header = await asyncio.wait_for(self._reader.readexactly(7), timeout=self._timeout)
        _tid, _proto, length, _unit = struct.unpack(">HHHB", header)
        pdu_len = length - 1
        data = await asyncio.wait_for(self._reader.readexactly(pdu_len), timeout=self._timeout)

        if data and (data[0] & 0x80):
            code = data[1] if len(data) > 1 else 0
            raise ModbusError(f"Exception from device (function={data[0] & 0x7F}, code={code})")

        return data

    async def _send_pdu(self, pdu: bytes) -> bytes:
        for attempt in range(1, self.retry_attempts + 2):
            try:
                return await self._send_pdu_once(pdu)
            except (asyncio.TimeoutError, asyncio.IncompleteReadError, ConnectionResetError, BrokenPipeError) as err:
                _LOGGER.debug("Modbus transport error on attempt %s: %r; reconnecting", attempt, err)
                await self.close()
                if attempt <= self.retry_attempts:
                    await asyncio.sleep(self.retry_delay)
                    continue
                raise

    async def read_holding_registers(self, address: int, count: int) -> List[int]:
        pdu = struct.pack(">BHH", 3, address, count)
        data = await self._send_pdu(pdu)
        byte_count = data[1]
        return list(struct.unpack(f">{byte_count // 2}H", data[2:2 + byte_count]))

    async def read_input_registers(self, address: int, count: int) -> List[int]:
        pdu = struct.pack(">BHH", 4, address, count)
        data = await self._send_pdu(pdu)
        byte_count = data[1]
        return list(struct.unpack(f">{byte_count // 2}H", data[2:2 + byte_count]))
