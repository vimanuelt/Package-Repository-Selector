# prs/config_manager.py

class ConfigManager:
    """
    A singleton class that stores config data purely in memory.
    Replaces any old file-based usage (e.g., config.ini).
    """

    _instance = None

    def __init__(self):
        # Holds all session data in memory only
        self._config_data = {}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get(self, key, default=None):
        return self._config_data.get(key, default)

    def set(self, key, value):
        self._config_data[key] = value

    def remove(self, key):
        self._config_data.pop(key, None)

    def print_all(self):
        print("[ConfigManager] Current in-memory config:")
        for k, v in self._config_data.items():
            print(f"  {k} = {v}")

