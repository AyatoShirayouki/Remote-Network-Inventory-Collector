# config.py

# Default SSH timeout in seconds
SSH_TIMEOUT = 5

# Thread pool max workers
MAX_WORKERS = 10

# Log file name
LOG_FILE = "collector.log"

# Retry logic (bonus feature)
RETRY_ATTEMPTS = 3
RETRY_BACKOFF = 2  # seconds

# Default interface filter if not provided by CLI
DEFAULT_INTERFACE_FILTERS = ["eth", "ens"]

# Command constants (can help with testing and command swaps)
COMMANDS = {
    "ROUTE": "ip route",
    "ADDRESS": "ip address"
}
