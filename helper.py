from storage import Storage
from command_security import Security

class Helper:
    def __init__(self, storage: Storage, command_security: Security):
        self.storage = storage
        self.command_security = command_security


