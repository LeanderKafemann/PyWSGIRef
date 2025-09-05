"""
BETA mode...
"""

from .exceptions import *
from .finished import OneWayBoolean

class beta:
    """
    BETA mode for PyWSGIRef.
    """
    def __init__(self):
        self._beta = False
        self.locked = OneWayBoolean()

    @property
    def value(self) -> bool:
        return self._beta

    def enable(self):
        """
        Enables BETA mode.
        """
        if self._beta:
            raise BetaAlreadyEnabledError()
        if self.locked.value:
            raise BetaAlreadyLocked()
        self._beta = True

    def lock(self):
        """
        Locks current value of beta
        """
        self.locked.set_true()

BETA = beta()

def enableBetaMode():
    """
    Enables BETA mode.
    """
    BETA.enable()
    print("BETA mode enabled.")