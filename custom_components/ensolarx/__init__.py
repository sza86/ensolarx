from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_SCAN_INTERVAL,
    CONF_SELECTED_REGISTERS,
    CONF_UNIT_ID,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    PLATFORMS,
    get_selected_sensor_defs,
)
from .coordinator import EnsolarXCoordinator
from .modbus_client import ModbusTcpClient

_LOGGER = logging.getLogger(__name__)


@dataclass
class EnsolarXRuntimeData:
    client: ModbusTcpClient
    coordinator: EnsolarXCoordinator


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up domain."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up EnsolarX from a config entry."""
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    unit_id = entry.data[CONF_UNIT_ID]
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))
    selected_registers = entry.options.get(CONF_SELECTED_REGISTERS)
    sensor_defs = get_selected_sensor_defs(selected_registers)

    client = ModbusTcpClient(host, port=port, unit_id=unit_id)
    coordinator = EnsolarXCoordinator(
        hass,
        client,
        sensor_defs=sensor_defs,
        scan_interval_s=scan_interval,
    )

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = EnsolarXRuntimeData(client=client, coordinator=coordinator)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.info(
        "EnsolarX: entry %s skonfigurowany (%s:%s, unit=%s, interval=%ss, rejestry=%s)",
        entry.entry_id,
        host,
        port,
        unit_id,
        scan_interval,
        len(sensor_defs),
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        runtime_data: EnsolarXRuntimeData = entry.runtime_data
        await runtime_data.client.close()
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload entry after options change."""
    await hass.config_entries.async_reload(entry.entry_id)
