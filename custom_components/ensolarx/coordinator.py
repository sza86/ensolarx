from __future__ import annotations

import asyncio
import logging
import struct
from datetime import timedelta
from typing import Any, Dict, List

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import MAX_BLOCK_SIZE, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class EnsolarXCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Koordynator odczytów Modbus dla EnsolarX."""

    def __init__(
        self,
        hass: HomeAssistant,
        client,
        sensor_defs: list[dict[str, Any]],
        scan_interval_s: int | None = None,
    ) -> None:
        interval = timedelta(seconds=scan_interval_s) if scan_interval_s else UPDATE_INTERVAL
        super().__init__(hass, _LOGGER, name="EnsolarX Coordinator", update_interval=interval)
        self.client = client
        self._defs = list(sensor_defs)
        self._last_ok: dict[str, Any] = {}
        self._retry_attempts: int = getattr(self.client, "retry_attempts", 1)
        self._retry_delay: float = getattr(self.client, "retry_delay", 0.15)

    async def _async_update_data(self) -> Dict[str, Any]:
        try:
            await self.client.connect()
            await asyncio.sleep(0)
        except Exception:
            _LOGGER.debug("EnsolarX: connect() failed before polling, first read will retry")

        results: dict[str, Any] = {}
        blocks = self._build_blocks(self._defs)

        for block in blocks:
            regs: list[int] | None = None
            try:
                regs = await self._read_block(block["input_type"], block["start"], block["count"])
            except Exception as err:
                _LOGGER.debug(
                    "EnsolarX: block read failed for %s %s:%s (%s), switching to per-register fallback",
                    block["input_type"],
                    block["start"],
                    block["count"],
                    err,
                )

            if regs is not None:
                for definition in block["sensors"]:
                    self._decode_from_block(results, definition, block["start"], regs)
                continue

            for definition in block["sensors"]:
                await self._read_single_sensor(results, definition)

        if not results:
            raise UpdateFailed("Modbus: nie udało się odczytać żadnego wybranego rejestru")

        return results

    async def _read_block(self, input_type: str, start: int, count: int) -> list[int]:
        last_err: Exception | None = None
        for attempt in range(1, self._retry_attempts + 2):
            try:
                if input_type == "holding":
                    return await self.client.read_holding_registers(start, count)
                return await self.client.read_input_registers(start, count)
            except Exception as err:
                last_err = err
                if attempt <= self._retry_attempts:
                    await asyncio.sleep(self._retry_delay)
        assert last_err is not None
        raise last_err

    async def _read_single_sensor(self, results: dict[str, Any], definition: dict[str, Any]) -> None:
        address = int(definition["address"])
        input_type = definition.get("input_type", "holding")
        fallback = bool(definition.get("fallback", True))
        count = self._register_count(definition)

        tried: list[str] = []
        reg_data: list[int] | None = None

        for kind in [input_type, "input" if input_type == "holding" else "holding"]:
            if kind != input_type and not fallback:
                break
            try:
                reg_data = await self._read_block(kind, address, count)
                tried.append(kind)
                break
            except Exception as err:
                tried.append(f"{kind}:{err}")

        if reg_data is None:
            self._restore_last_value(results, definition)
            _LOGGER.warning(
                "EnsolarX: problem z adresem %s (%s), próby=%s",
                address,
                definition["name"],
                "; ".join(tried),
            )
            return

        self._decode_and_store(results, definition, reg_data)

    def _decode_from_block(
        self,
        results: dict[str, Any],
        definition: dict[str, Any],
        block_start: int,
        block_regs: list[int],
    ) -> None:
        address = int(definition["address"])
        count = self._register_count(definition)
        offset = address - block_start
        regs = block_regs[offset: offset + count]
        if len(regs) != count:
            self._restore_last_value(results, definition)
            _LOGGER.warning("EnsolarX: blok nie zawiera kompletnych danych dla adresu %s", address)
            return
        self._decode_and_store(results, definition, regs)

    def _decode_and_store(self, results: dict[str, Any], definition: dict[str, Any], regs: list[int]) -> None:
        name = definition["name"]
        address = int(definition["address"])
        dtype = definition.get("dtype") or definition.get("data_type", "uint16")
        scale = float(definition.get("scale", 1.0))
        precision = definition.get("precision")
        word_swap = bool(definition.get("word_swap", False))

        try:
            value = self._decode_registers(regs, dtype, word_swap)
        except Exception as err:
            self._restore_last_value(results, definition)
            _LOGGER.warning("EnsolarX: błąd dekodowania adresu %s (%s): %s", address, name, err)
            return

        if scale != 1.0:
            value = value * scale
        if precision is not None and isinstance(value, (int, float)):
            value = round(value, int(precision))

        results[name] = value
        results[str(address)] = value
        self._last_ok[name] = value
        self._last_ok[str(address)] = value

    def _restore_last_value(self, results: dict[str, Any], definition: dict[str, Any]) -> None:
        name = definition["name"]
        address = str(definition["address"])
        if name in self._last_ok:
            results[name] = self._last_ok[name]
            results[address] = self._last_ok[address]

    @staticmethod
    def _register_count(definition: dict[str, Any]) -> int:
        dtype = definition.get("dtype") or definition.get("data_type", "uint16")
        return 1 if dtype in ("uint16", "int16") else 2

    @staticmethod
    def _decode_registers(regs: List[int], dtype: str, word_swap: bool) -> Any:
        if dtype == "uint16":
            return int(regs[0] & 0xFFFF)

        if dtype == "int16":
            value = regs[0]
            if value & 0x8000:
                value -= 0x10000
            return int(value)

        if dtype in ("uint32", "float32"):
            if len(regs) < 2:
                raise ValueError("brak dwóch rejestrów dla wartości 32-bit")
            hi, lo = regs[0], regs[1]
            if word_swap:
                hi, lo = lo, hi
            raw = (hi << 16) | lo
            if dtype == "uint32":
                return int(raw & 0xFFFFFFFF)
            return struct.unpack(">f", raw.to_bytes(4, "big"))[0]

        raise ValueError(f"Nieznany data_type: {dtype}")

    @staticmethod
    def _build_blocks(sensor_defs: list[dict[str, Any]]) -> list[dict[str, Any]]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for definition in sensor_defs:
            grouped.setdefault(definition.get("input_type", "holding"), []).append(definition)

        blocks: list[dict[str, Any]] = []
        for input_type, definitions in grouped.items():
            sorted_defs = sorted(definitions, key=lambda item: int(item["address"]))
            current: dict[str, Any] | None = None

            for definition in sorted_defs:
                start = int(definition["address"])
                end = start + EnsolarXCoordinator._register_count(definition) - 1

                if current is None:
                    current = {
                        "input_type": input_type,
                        "start": start,
                        "end": end,
                        "count": end - start + 1,
                        "sensors": [definition],
                    }
                    continue

                next_count = max(current["end"], end) - current["start"] + 1
                if start <= current["end"] + 1 and next_count <= MAX_BLOCK_SIZE:
                    current["end"] = max(current["end"], end)
                    current["count"] = current["end"] - current["start"] + 1
                    current["sensors"].append(definition)
                else:
                    blocks.append(current)
                    current = {
                        "input_type": input_type,
                        "start": start,
                        "end": end,
                        "count": end - start + 1,
                        "sensors": [definition],
                    }

            if current is not None:
                blocks.append(current)

        return blocks
