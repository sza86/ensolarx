from __future__ import annotations

from datetime import timedelta
from typing import Any

DOMAIN = "ensolarx"

CONF_UNIT_ID = "unit_id"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_SELECTED_REGISTERS = "selected_registers"

DEFAULT_PORT = 4196
DEFAULT_UNIT_ID = 18
DEFAULT_SCAN_INTERVAL = 10
MIN_SCAN_INTERVAL = 5
MAX_BLOCK_SIZE = 20

PLATFORMS = ["sensor"]
UPDATE_INTERVAL = timedelta(seconds=DEFAULT_SCAN_INTERVAL)

# Pełna lista dostępnych definicji rejestrów.
# Użytkownik wybiera, które z nich mają zostać utworzone jako encje.
SENSOR_DEFS: list[dict[str, Any]] = [
    {"name": "Moc wejścia PV1", "address": 1, "unit": "W", "data_type": "uint16", "device_class": "power", "state_class": "measurement"},
    {"name": "Całkowita moc PV", "address": 3, "unit": "W", "data_type": "uint16", "device_class": "power", "state_class": "measurement"},
    {"name": "Napięcie PV1", "address": 4, "unit": "V", "data_type": "uint16", "scale": 0.1, "precision": 1, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Prąd PV1", "address": 5, "unit": "A", "data_type": "int16", "scale": 0.1, "precision": 1, "device_class": "current", "state_class": "measurement"},
    {"name": "Napięcie sieci L1", "address": 8, "unit": "V", "data_type": "uint16", "scale": 0.1, "precision": 1, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Moc obciążenia L1", "address": 11, "unit": "W", "data_type": "uint16", "device_class": "power", "state_class": "measurement"},
    {"name": "Całkowita moc obciążenia", "address": 14, "unit": "W", "data_type": "uint16", "device_class": "power", "state_class": "measurement"},
    {"name": "Procent obciążenia", "address": 15, "unit": "%", "data_type": "uint16", "state_class": "measurement"},
    {"name": "Napięcie obciążenia", "address": 16, "unit": "V", "data_type": "uint16", "device_class": "voltage", "state_class": "measurement"},
    {"name": "Napięcie baterii", "address": 17, "unit": "V", "data_type": "uint16", "scale": 0.1, "precision": 1, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Prąd baterii", "address": 18, "unit": "A", "data_type": "int16", "scale": 0.1, "precision": 1, "device_class": "current", "state_class": "measurement"},
    {"name": "Status inwertera", "address": 23, "data_type": "uint16"},
    {"name": "Tryb pracy inwertera", "address": 24, "data_type": "uint16"},
    {"name": "Priorytet ładowania", "address": 25, "data_type": "uint16"},
    {"name": "Powrót po niskim napięciu", "address": 29, "unit": "V", "data_type": "uint16", "scale": 0.1, "precision": 1, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Powrót rozładowywania", "address": 30, "unit": "V", "data_type": "uint16", "scale": 0.1, "precision": 1, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Procent baterii (if)", "address": 34, "unit": "%", "data_type": "uint16", "state_class": "measurement"},
    {"name": "Prąd baterii (if)", "address": 35, "unit": "A", "data_type": "int16", "device_class": "current", "state_class": "measurement"},
    {"name": "Status ładowania z sieci 1", "address": 36, "data_type": "uint16"},
    {"name": "Status PV = U * I", "address": 45, "data_type": "uint16"},
    {"name": "Temperatura radiatora", "address": 46, "unit": "°C", "data_type": "int16", "device_class": "temperature", "state_class": "measurement"},
    {"name": "SOC baterii", "address": 57, "unit": "%", "data_type": "uint16", "scale": 0.1, "precision": 1, "state_class": "measurement"},
    {"name": "Pozostały prąd baterii", "address": 58, "unit": "Ah", "data_type": "int16", "state_class": "measurement"},
    {"name": "Różnica napięć celi", "address": 62, "unit": "V", "data_type": "uint16", "scale": 0.001, "precision": 3, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Stan MOSFETów", "address": 63, "data_type": "uint16"},
    {"name": "Napięcie celi 1", "address": 70, "unit": "V", "data_type": "uint16", "scale": 0.001, "precision": 3, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Napięcie celi 2", "address": 71, "unit": "V", "data_type": "uint16", "scale": 0.001, "precision": 3, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Napięcie celi 3", "address": 72, "unit": "V", "data_type": "uint16", "scale": 0.001, "precision": 3, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Napięcie celi 4", "address": 73, "unit": "V", "data_type": "uint16", "scale": 0.001, "precision": 3, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Napięcie celi 5", "address": 74, "unit": "V", "data_type": "uint16", "scale": 0.001, "precision": 3, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Napięcie celi 6", "address": 75, "unit": "V", "data_type": "uint16", "scale": 0.001, "precision": 3, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Napięcie celi 7", "address": 76, "unit": "V", "data_type": "uint16", "scale": 0.001, "precision": 3, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Napięcie celi 8", "address": 77, "unit": "V", "data_type": "uint16", "scale": 0.001, "precision": 3, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Napięcie celi 9", "address": 78, "unit": "V", "data_type": "uint16", "scale": 0.001, "precision": 3, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Napięcie celi 10", "address": 79, "unit": "V", "data_type": "uint16", "scale": 0.001, "precision": 3, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Napięcie celi 11", "address": 80, "unit": "V", "data_type": "uint16", "scale": 0.001, "precision": 3, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Napięcie celi 12", "address": 81, "unit": "V", "data_type": "uint16", "scale": 0.001, "precision": 3, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Napięcie celi 13", "address": 82, "unit": "V", "data_type": "uint16", "scale": 0.001, "precision": 3, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Napięcie celi 14", "address": 83, "unit": "V", "data_type": "uint16", "scale": 0.001, "precision": 3, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Napięcie celi 15", "address": 84, "unit": "V", "data_type": "uint16", "scale": 0.001, "precision": 3, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Napięcie celi 16", "address": 85, "unit": "V", "data_type": "uint16", "scale": 0.001, "precision": 3, "device_class": "voltage", "state_class": "measurement"},
    {"name": "Temperatura BMS 1", "address": 86, "unit": "°C", "data_type": "int16", "device_class": "temperature", "state_class": "measurement"},
    {"name": "Stan BMS", "address": 87, "data_type": "uint16"},
    {"name": "Przekroczenie napięcia celi", "address": 88, "data_type": "uint16"},
    {"name": "Temperatura akumulatora", "address": 95, "unit": "°C", "data_type": "int16", "device_class": "temperature", "state_class": "measurement"},
    {"name": "Dziennie: Napięcie sieci", "address": 117, "unit": "V", "data_type": "uint16", "device_class": "voltage", "state_class": "measurement"},
    {"name": "Dziennie: Moc PV", "address": 118, "unit": "W", "data_type": "uint16", "device_class": "power", "state_class": "measurement"},
    {"name": "Dziennie: Moc wyjściowa", "address": 119, "unit": "W", "data_type": "uint16", "device_class": "power", "state_class": "measurement"},
    {"name": "Dziennie: Napięcie baterii", "address": 120, "unit": "V", "data_type": "uint16", "device_class": "voltage", "state_class": "measurement"},
    {"name": "Dziennie: Ładowanie", "address": 121, "unit": "W", "data_type": "int16", "device_class": "power", "state_class": "measurement"},
    {"name": "Dziennie: Rozładowanie", "address": 122, "unit": "W", "data_type": "int16", "device_class": "power", "state_class": "measurement"},
    {"name": "Dziennie: Do sieci", "address": 123, "unit": "W", "data_type": "int16", "device_class": "power", "state_class": "measurement"},
    {"name": "Dziennie: Z sieci", "address": 124, "unit": "W", "data_type": "int16", "device_class": "power", "state_class": "measurement"},
    {"name": "Dziennie: Ładowanie battery first", "address": 125, "unit": "W", "data_type": "int16", "device_class": "power", "state_class": "measurement"},
    {"name": "Dziennie: Ładowanie output first", "address": 126, "unit": "W", "data_type": "int16", "device_class": "power", "state_class": "measurement"},
    {"name": "RTC rok", "address": 127, "data_type": "uint16"},
    {"name": "RTC miesiąc", "address": 128, "data_type": "uint16"},
    {"name": "RTC dzień", "address": 129, "data_type": "uint16"},
    {"name": "RTC godzina", "address": 130, "data_type": "uint16"},
    {"name": "RTC minuta", "address": 131, "data_type": "uint16"},
    {"name": "RTC sekunda", "address": 132, "data_type": "uint16"},
    {"name": "Temperatura BMS 2", "address": 133, "unit": "°C", "data_type": "int16", "device_class": "temperature", "state_class": "measurement"},
    {"name": "Wersja firmware", "address": 134, "data_type": "uint16"},
    {"name": "Wersja firmware WiFi", "address": 135, "data_type": "uint16"},
]

SENSOR_BY_ADDRESS: dict[int, dict[str, Any]] = {item["address"]: item for item in SENSOR_DEFS}
REGISTER_OPTIONS: dict[str, str] = {
    str(item["address"]): f'{item["address"]} — {item["name"]}' for item in SENSOR_DEFS
}
ALL_REGISTER_KEYS: list[str] = [str(item["address"]) for item in SENSOR_DEFS]


def normalize_selected_registers(selected: list[str] | tuple[str, ...] | None) -> list[str]:
    """Zwróć posortowaną listę poprawnych kluczy rejestrów."""
    if not selected:
        return ALL_REGISTER_KEYS.copy()

    valid = {str(addr) for addr in SENSOR_BY_ADDRESS}
    cleaned = sorted({key for key in selected if key in valid}, key=lambda x: int(x))
    return cleaned or ALL_REGISTER_KEYS.copy()


def get_selected_sensor_defs(selected: list[str] | tuple[str, ...] | None) -> list[dict[str, Any]]:
    """Zwróć definicje sensorów dla wybranych rejestrów."""
    return [SENSOR_BY_ADDRESS[int(key)] for key in normalize_selected_registers(selected)]
