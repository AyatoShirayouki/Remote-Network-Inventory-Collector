# tests/test_utils.py

import pytest
import time
from network_inventory_collector.utils import retry_with_backoff

def test_retry_with_backoff_success():
    calls = []

    @retry_with_backoff
    def flaky():
        calls.append(1)
        if len(calls) < 2:
            raise ValueError("fail once")
        return "success"

    assert flaky() == "success"
    assert len(calls) == 2
