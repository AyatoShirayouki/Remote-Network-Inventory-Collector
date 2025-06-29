# Remote Network Inventory Collector

## Overview
This is a Python-based tool that connects to one or more remote Linux servers over SSH, using multiple potential credentials or SSH keys.
Once connected, it:
    - Retrieves each host’s routing table (`ip route`)
    - Retrieves network interfaces and IP addresses (`ip address`)
    - Parses and structures the output in JSON
    - Supports multithreading for speed
    - Provides safe logging, retry with backoff, and SSH key fallback for robust operation.

## Features
- Tries each host with multiple usernames/passwords until one works.
- Falls back to SSH key authentication automatically if passwords fail.
- Runs `ip route` and `ip address` securely.
- Parses all output into structured JSON — now robustly handles leading/trailing whitespace in real SSH output.
- Optional interface name filtering (e.g., only `eth*` or `ens*`).
- Multithreaded for high performance when scanning multiple hosts.
- Logs to both `collector.log` and the console for easy debugging.
- Includes retry logic with exponential backoff on connection or command execution failures.
- Full test suite with `pytest` and realistic test data.


## Project Structure

RemoteNetworkInventoryCollector/
├── network_inventory_collector/
│   ├── __init__.py        # Package version & metadata
│   ├── main.py            # Entry point — CLI, threading, output
│   ├── collector.py       # Orchestrates per-host SSH, commands, parsing
│   ├── ssh_client.py      # Handles SSH connection & fallback logic
│   ├── parser.py          # Parses `ip route` and `ip address` output (now robust to whitespace)
│   ├── models.py          # Dataclass for structured JSON output
│   ├── utils.py           # Helpers: file I/O, logger setup, retry decorator
│   ├── config.py          # Global constants: timeouts, retries, commands, filters
├── tests/                 # All unit tests with pytest
│   ├── test_collector.py
│   ├── test_parser.py
│   ├── test_ssh_client.py
│   ├── test_utils.py
├── hosts.txt              # List of hosts to connect to (one per line)
├── credentials.txt        # List of credentials (username=password per line)
├── output.json            # Optional JSON output file
├── collector.log          # Log file with connection details & errors
├── requirements.txt       # Production dependencies (e.g., paramiko)
├── pytest.ini             # Pytest config: sets pythonpath for local tests
├── venv/                  # Your virtual environment (should be gitignored)


## What each file does
__`main.py`__
    - Handles argument parsing (`--hosts`, `--credentials`, `--output`, `--interface-filter`)
    - Calls `setup_logger` for logging to file & console.
    - Loads hosts and credentials.
    - Uses a `ThreadPoolExecutor` to run multiple SSH connections concurrently.
    - Collects and prints the final structured JSON.
    - Optionally writes to `output.json`.

__`collector.py`__
    - Defines `collect_from_host()`:
        - Loops through each username/password combination.
        - If no password works, tries SSH key fallback.
        - Once connected:
            - Runs `ip route` and `ip address` using `safe_exec()`, which retries on failures.
            - Parses the outputs.
            - Builds a structured `HostData` object.
    - Implements `safe_exec` with `@retry_with_backoff`.

__`ssh_client.py`__
    - Defines `try_ssh_connection()`:
        - Connects to SSH using Paramiko.
        - Handles timeouts, unreachable hosts, and authentication errors.
        - Uses a retry decorator for connection resilience.
        - Supports both password-based and key-based authentication (fallback).

__`parser.py`__
    - Defines `parse_ip_route()`:
      - Parses the raw text output of `ip route` into a list of route dictionaries.
    - Defines `parse_ip_address()`:
      - Parses the output of `ip address` into structured interface dictionaries.
      - Now strips leading/trailing spaces for real-world robustness.
      - Supports optional interface name filtering (`eth*`, `ens*`, etc.).
      - Extracts both IPv4 (`inet`) and IPv6 (`inet6`) addresses for each interface.


__`models.py`__
    - Defines a `HostData` dataclass:
        - Stores `host`, `routing_table`, and `interfaces`.
        - Provides `to_dict()` for easy JSON serialization.

__`utils.py`__
    - `load_hosts()`: Reads your `hosts.txt` file.
    - `load_credentials()`: Reads your `credentials.txt` file.
    - `setup_logger()`: Configures logging to `collector.log` and the console.
    - `retry_with_backoff`: Decorator for retrying any function with exponential backoff.

__`config.py`__
    - Holds constants:
        - SSH timeout.
        - Max threads.
        - Log file name.
        - Retry attempts and backoff settings.
        - Default interface filters.
        - Command strings for `ip route` and `ip address`.

__`__init__.py`__
Defines your package version and author:
```python
__version__ = "1.0.0"
__author__ = "Aleksandar Nestorov"
```

## How to Set Up and Run

### 1️ Clone or Download the Project

Put your Python files into a project folder like this:

RemoteNetworkInventoryCollector/
├── network_inventory_collector/
│   ├── __init__.py
│   ├── main.py
│   ├── collector.py
│   ├── ssh_client.py
│   ├── parser.py
│   ├── models.py
│   ├── utils.py
│   ├── config.py
├── tests/
│   ├── test_collector.py
│   ├── test_parser.py
│   ├── test_ssh_client.py
│   ├── test_utils.py
├── hosts.txt              # Input: list of hosts (one per line)
├── credentials.txt        # Input: credentials (username=password)
├── requirements.txt       # Your Python dependencies (paramiko, pytest)
├── pytest.ini             # Pytest config for test discovery
├── output.json            # (Optional) final JSON output file
├── collector.log          # Log file with connection details and errors
└── venv/                  # Your virtual environment (should be gitignored)


### 2. Create aor Activate a Virtual Environment
```python
# Create the venv
python3 -m venv venv

# Activate it
source venv/bin/activate   # macOS/Linux

# On Windows:
# venv\Scripts\activate

```

### 3. Install Dependencies
Run: `pip install -r requirements.txt`

### 4. Prepare Your Input Files
`hosts.txt`:
One hostname or IP per line. Example for a free public test SSH server: `test.rebex.net`

`credentials.txt`:
Each line: `username=password`
Example: `demo=password`

### 5. Run the Inventory Collector
```bash
python network_inventory_collector/main.py \
  --hosts hosts.txt \
  --credentials credentials.txt \
  --output output.json \
  --interface-filter eth,ens
```

__Arguments__:
    - `--hosts`: Path to your hosts file.
    - `--credentials`: Path to your credentials file.
    - `--output`: (Optional) Save the JSON result to a file.
    - `--interface-filter`: (Optional) Only include interfaces that match these prefixes.

### Example Test Server
    - For testing, use the Rebex public SSH test server:
        - `Host`: test.rebex.net
        - `Username`: demo
        - `Password`: password

To verify manually:
```bash
ssh demo@test.rebex.net
```
### What You’ll See
    - Pretty-printed JSON output in your terminal.
    - An optional `output.json` file if you use `--output`.
    - A `collector.log` file with detailed connection logs and any errors.

### How the Tool Handles Failures
    - If an SSH connection fails, it automatically retries with backoff.
    - If password auth fails, it tries SSH key auth.
    - Errors like timeouts or bad credentials are logged safely.
    - You’ll never lose other hosts’ results due to one failure.

### Example JSON Output
```json
[
  {
    "host": "test.rebex.net",
    "routing_table": [
      { "raw": "default via 192.168.1.1 dev eth0", "type": "default" },
      { "raw": "192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.10" }
    ],
    "interfaces": [
      {
        "name": "eth0",
        "addresses": ["192.168.1.10/24"]
      }
    ]
  }
]
```
### Output Files
| File              | What it Contains                      |
| ----------------- | ------------------------------------- |
| `output.json`     | Final structured network inventory    |
| `collector.log`   | All SSH attempts, retries, and errors |
| `hosts.txt`       | One IP or hostname per line           |
| `credentials.txt` | One `username=password` per line      |

## Test Suite Overview

This project includes a complete unit test suite using `pytest` to ensure that your SSH logic, parsing, and retry behavior are reliable and robust.  
All test files live under the `tests/` folder.

### `tests/` Contents

| File                  | What It Tests                                                            |
|-----------------------|---------------------------------------------------------------------------|
| `test_collector.py`   | Tests the `collect_from_host()` orchestration logic using mocks.<br>Ensures SSH connection attempts, fallback to SSH keys, command execution, and parsing flow all work together correctly. |
| `test_parser.py`      | Tests `parse_ip_route()` and `parse_ip_address()` with realistic sample outputs.<br>Verifies both IPv4/IPv6 address extraction and the fix for handling leading/trailing whitespace. |
| `test_ssh_client.py`  | Tests `try_ssh_connection()` with `paramiko` mocked.<br>Ensures connection success paths and retry decorator work without real SSH servers. |
| `test_utils.py`       | Tests the `retry_with_backoff` decorator to ensure retry logic and exponential backoff run as expected for flaky operations. |

### Key Points
- The tests **mock SSH connections** so you don’t need live servers.
- The parser tests use real-like `ip route` and `ip address` outputs to catch edge cases.
- `pytest.ini` sets `pythonpath = .` to ensure tests always find your `network_inventory_collector` package.
- All tests can be run in one step:  
```bash
  pytest
```

## How to Run the Tests

This project includes unit tests covering:
- SSH connection logic (mocked)
- Output parsing for both `ip route` and `ip address`
- Retry logic for backoff scenarios
- The full `collect_from_host` flow with mocks

### 1. Add a `pytest.ini` to the project root:
```ini
[pytest]
python_files = tests/test_*.py
pythonpath = .

