import yaml


class Configuration:
    """Loads the given configuration into the 'data' property"""

    def __init__(self, configPath):
        self._data = yaml.load(open(configPath, 'rb').read())

    @property
    def data(self):
        "Access loaded configuration data as a dictionary"
        return self._data
