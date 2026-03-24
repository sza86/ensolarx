from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers import config_validation as cv

from .const import (
    ALL_REGISTER_KEYS,
    CONF_SCAN_INTERVAL,
    CONF_SELECTED_REGISTERS,
    CONF_UNIT_ID,
    DEFAULT_PORT,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_UNIT_ID,
    DOMAIN,
    MIN_SCAN_INTERVAL,
    REGISTER_OPTIONS,
)
from .modbus_client import ModbusTcpClient


async def _validate_connection(host: str, port: int, unit_id: int) -> None:
    client = ModbusTcpClient(host, port=port, unit_id=unit_id)
    await client.connect()
    await client.close()


class EnsolarXConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for EnsolarX."""

    VERSION = 2
    MINOR_VERSION = 0

    def __init__(self) -> None:
        self._user_data: dict[str, Any] = {}

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                await _validate_connection(
                    user_input[CONF_HOST],
                    user_input[CONF_PORT],
                    user_input[CONF_UNIT_ID],
                )
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                self._user_data = user_input
                unique_id = f"{user_input[CONF_HOST]}:{user_input[CONF_PORT]}:{user_input[CONF_UNIT_ID]}"
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()
                return await self.async_step_registers()

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
                vol.Required(CONF_UNIT_ID, default=DEFAULT_UNIT_ID): int,
                vol.Required(CONF_SCAN_INTERVAL): vol.All(int, vol.Range(min=MIN_SCAN_INTERVAL)),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_registers(self, user_input: dict[str, Any] | None = None):
        errors: dict[str, str] = {}

        if user_input is not None:
            selected_registers = sorted(user_input[CONF_SELECTED_REGISTERS], key=int)
            if not selected_registers:
                errors["base"] = "select_at_least_one_register"
            else:
                return self.async_create_entry(
                    title=f"EnsolarX {self._user_data[CONF_HOST]}",
                    data=self._user_data,
                    options={CONF_SELECTED_REGISTERS: selected_registers},
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_SELECTED_REGISTERS, default=[]): cv.multi_select(REGISTER_OPTIONS)
            }
        )
        return self.async_show_form(step_id="registers", data_schema=schema, errors=errors)

    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return EnsolarXOptionsFlow(config_entry)

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None):
        entry = self._get_reconfigure_entry()
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                await _validate_connection(
                    user_input[CONF_HOST],
                    user_input[CONF_PORT],
                    user_input[CONF_UNIT_ID],
                )
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                return self.async_update_reload_and_abort(
                    entry,
                    data_updates=user_input,
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default=entry.data[CONF_HOST]): str,
                vol.Required(CONF_PORT, default=entry.data[CONF_PORT]): int,
                vol.Required(CONF_UNIT_ID, default=entry.data[CONF_UNIT_ID]): int,
                vol.Required(
                    CONF_SCAN_INTERVAL,
                    default=entry.options.get(CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)),
                ): vol.All(int, vol.Range(min=MIN_SCAN_INTERVAL)),
            }
        )
        return self.async_show_form(step_id="reconfigure", data_schema=schema, errors=errors)


class EnsolarXOptionsFlow(config_entries.OptionsFlow):
    """Handle EnsolarX options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input: Mapping[str, Any] | None = None):
        errors: dict[str, str] = {}

        if user_input is not None:
            selected_registers = sorted(user_input[CONF_SELECTED_REGISTERS], key=int)
            if not selected_registers:
                errors["base"] = "select_at_least_one_register"
            else:
                return self.async_create_entry(
                    title="",
                    data={
                        CONF_SCAN_INTERVAL: user_input[CONF_SCAN_INTERVAL],
                        CONF_SELECTED_REGISTERS: selected_registers,
                    },
                )

        selected = self.config_entry.options.get(CONF_SELECTED_REGISTERS, ALL_REGISTER_KEYS)
        scan_interval = self.config_entry.options.get(
            CONF_SCAN_INTERVAL,
            self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )

        schema = vol.Schema(
            {
                vol.Required(CONF_SCAN_INTERVAL, default=scan_interval): vol.All(int, vol.Range(min=MIN_SCAN_INTERVAL)),
                vol.Required(CONF_SELECTED_REGISTERS, default=selected): cv.multi_select(REGISTER_OPTIONS),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema, errors=errors)
