from .finished import OneWayBoolean
from .exceptions import ServerAlreadyGeneratedError
from .pyhtml import PyHTML

class MacroDict:
    """
    A dictionary to store macros for the PyWSGIRef framework.
    """
    def __init__(self):
        self.macros = {}
        self.locked = OneWayBoolean()

    def __getitem__(self, key: str) -> str:
        return self.macros[key]
    
    def __setitem__(self, key: str, value: PyHTML):
        if not isinstance(value, PyHTML):
            raise TypeError("Value must be an instance of PyHTML.")
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")
        if self.locked.value:
            raise ServerAlreadyGeneratedError("Cannot modify macros after it has been locked.")
        self.macros[key] = value.decoded()
    
    def __contains__(self, key: str):
        return key in self.macros
    
    def __repr__(self):
        return f"MacroDict({self.macros})"
    
    def keys(self) -> list:
        return list(self.macros.keys())
    
    def values(self) -> list:
        return list(self.macros.values())
    
    def get(self, key: str, default=None) -> str:
        return self.macros.get(key, default)
    
    def items(self) -> list:
        return list(self.macros.items())