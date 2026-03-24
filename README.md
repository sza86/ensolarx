# EnsolarX Modbus TCP dla Home Assistant

Niestandardowa integracja Home Assistant do odczytu urządzeń EnsolarX przez Modbus TCP.

Integracja została przygotowana z myślą o użytkownikach, którzy chcą samodzielnie wybrać dokładnie te rejestry, które mają być odczytywane — zarówno podczas pierwszej konfiguracji, jak i później z poziomu opcji integracji.

## Najważniejsze funkcje

- konfiguracja z poziomu interfejsu Home Assistant (`config_flow`),
- weryfikacja połączenia Modbus TCP podczas dodawania integracji,
- wybór pojedynczych rejestrów podczas pierwszej konfiguracji,
- możliwość zmiany wybranych rejestrów po instalacji z poziomu opcji integracji,
- odczyt rejestrów w blokach ciągłych w celu zmniejszenia obciążenia Modbus,
- automatyczny fallback do odczytów pojedynczych rejestrów w przypadku błędu odczytu bloku,
- tłumaczenia w języku polskim i angielskim,
- obsługa diagnostyki integracji,
- gotowość do instalacji ręcznej oraz przez HACS jako repozytorium niestandardowe.

## Instalacja

### Opcja 1: HACS

1. Otwórz **HACS**.
2. Przejdź do **Niestandardowe repozytoria**.
3. Dodaj to repozytorium jako **Integrację**.
4. Zainstaluj **EnsolarX Modbus TCP**.
5. Uruchom ponownie Home Assistant.
6. Przejdź do **Ustawienia → Urządzenia i usługi → Dodaj integrację**.
7. Wyszukaj **EnsolarX Modbus TCP**.

### Opcja 2: instalacja ręczna

1. Pobierz to repozytorium.
2. Skopiuj katalog `custom_components/ensolarx` do katalogu konfiguracyjnego Home Assistant:

```text
<config>/custom_components/ensolarx
```

3. Uruchom ponownie Home Assistant.
4. Przejdź do **Ustawienia → Urządzenia i usługi → Dodaj integrację**.
5. Wyszukaj **EnsolarX Modbus TCP**.

## Konfiguracja

Podczas pierwszego uruchomienia integracja korzysta z dwuetapowego kreatora konfiguracji.

### Krok 1: ustawienia połączenia

Użytkownik podaje:

- adres hosta / IP,
- port TCP,
- Unit ID / Slave ID,
- interwał odczytu.

Wartości domyślne:

- **Port:** `4196`
- **Unit ID:** `18`

### Krok 2: wybór rejestrów

Integracja wyświetla pełną listę obsługiwanych rejestrów.
Tworzone są wyłącznie encje dla rejestrów zaznaczonych przez użytkownika.

Po instalacji wybrane rejestry oraz interwał odczytu można zmienić z poziomu opcji integracji.

## Sposób odczytu danych

Aby ograniczyć ruch Modbus i poprawić stabilność działania, integracja grupuje sąsiadujące rejestry w ciągłe bloki i odczytuje je większymi żądaniami.

Jeżeli odczyt bloku się nie powiedzie, integracja automatycznie ponawia próbę w trybie pojedynczych odczytów dla problematycznego fragmentu.

## Diagnostyka i logowanie

Integracja obsługuje diagnostykę Home Assistant, co ułatwia analizę problemów.

Aby włączyć logowanie diagnostyczne, dodaj do pliku `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.ensolarx: debug
```

## Struktura repozytorium

```text
.
├── custom_components/
│   └── ensolarx/
│       ├── __init__.py
│       ├── config_flow.py
│       ├── const.py
│       ├── coordinator.py
│       ├── diagnostics.py
│       ├── manifest.json
│       ├── modbus_client.py
│       ├── sensor.py
│       ├── brand/
│       │   ├── icon.png
│       │   └── logo.png
│       └── translations/
│           ├── en.json
│           └── pl.json
├── hacs.json
├── LICENSE
└── README.md
```

## Zgodność

Integracja została przygotowana dla współczesnych wersji Home Assistant opartych o config entries oraz `runtime_data`.

## Zgłaszanie problemów

Przy zgłoszeniu błędu warto dołączyć:

- wersję Home Assistant,
- wersję integracji,
- model urządzenia,
- listę wybranych rejestrów,
- dane diagnostyczne lub logi debug.

## Zastrzeżenie

Projekt jest nieoficjalną integracją niestandardową i nie jest powiązany z firmą EnsolarX ani przez nią wspierany.

## Licencja

Projekt jest udostępniany na licencji MIT. Szczegóły znajdują się w pliku `LICENSE`.
