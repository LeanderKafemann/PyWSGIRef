"""
BETA mode...
"""

from .exceptions import BetaAlreadyEnabledError

class beta:
    """
    BETA mode for PyWSGIRef.
    """
    def __init__(self):
        self._beta = False

    @property
    def value(self) -> bool:
        return self._beta

    def enable(self):
        """
        Enables BETA mode.
        """
        if self._beta:
            raise BetaAlreadyEnabledError()
        self._beta = True

BETA = beta()

def enableBetaMode():
    """
    Enables BETA mode.
    """
    BETA.enable()
    print("BETA mode enabled.")