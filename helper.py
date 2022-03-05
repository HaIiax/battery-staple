from storage import Storage
from command_security import Security
from location_normalizer import LocationNormalizer

class Helper:
    def __init__(self, storage: Storage, command_security: Security, location_normalizer: LocationNormalizer):
        self.storage = storage
        self.command_security = command_security
        self.location_normalizer = location_normalizer


