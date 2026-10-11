"""Shared config for digital-twin-framework.

All tools read TWIN_HOME from environment, defaulting to ~/.twin.
Override with: export TWIN_HOME=/path/to/your/twin
"""
import os

def home():
    return os.path.expanduser(os.getenv("TWIN_HOME", "~/.twin"))

def data_path(name):
    d = os.path.join(home(), "data")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, name)
