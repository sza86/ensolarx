from __future__ import annotations

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant

from . import EnsolarXRuntimeData
from .const import CONF_SCAN_INTERVAL, CONF_SELECTED_REGISTERS, CONF_UNIT_ID, DOMAIN

TO_REDACT = {CONF_HOST}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""
    runtime_data: EnsolarXRuntimeData = entry.runtime_data
    coordinator = runtime_data.coordinator

    payload = {
        "domain": DOMAIN,
        "entry": {
            "entry_id": entry.entry_id,
            "title": entry.title,
            "data": dict(entry.data),
            "options": dict(entry.options),
        },
        "connection": {
            "host": entry.data.get(CONF_HOST),
            "port": entry.data.get(CONF_PORT),
            "unit_id": entry.data.get(CONF_UNIT_ID),
            "scan_interval": entry.options.get(
                CONF_SCAN_INTERVAL,
                entry.data.get(CONF_SCAN_INTERVAL),
            ),
        },
        "selected_registers": entry.options.get(CONF_SELECTED_REGISTERS, []),
        "selected_register_count": len(entry.options.get(CONF_SELECTED_REGISTERS, [])),
        "last_update_success": coordinator.last_update_success,
        "available_values": sorted((coordinator.data or {}).keys()),
    }
    return async_redact_data(payload, TO_REDACT)
