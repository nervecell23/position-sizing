import pytest
import os

@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("TESTING", "TRUE")
