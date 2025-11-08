class ServerAlreadyGeneratedError(Exception):
    """
    Raised when a server is already generated,
    so that further modifications are not allowed.
    """
    def __init__(self, message="Server has already been generated."):
        self.message = message
        super().__init__(self.message)

class InvalidFiletypeError(Exception):
    """
    Raised when an invalid file type (not PyHTML) is encountered.
    """
    def __init__(self, message="Invalid file type. Only .pyhtml files are allowed."):
        self.message = message
        super().__init__(self.message)

class InvalidCallableError(Exception):
    """
    Raised when a callable is expected but not provided.
    """
    def __init__(self, message="Expected a callable object."):
        self.message = message
        super().__init__(self.message)

class AdvancedHeadersWithoutAdvancedModeError(Exception):
    """
    Raised when advanced headers are set without advanced mode being enabled.
    """
    def __init__(self, message="Advanced headers cannot be set without enabling advanced mode."):
        self.message = message
        super().__init__(self.message)

class InvalidIncludePhraseFiletypeError(InvalidFiletypeError):
    """
    Raised when an invalid file type is encountered in the include phrase of a PyHTML file.
    """
    def __init__(self, message="Invalid file type in include phrase. Only .css, .js, and .json files are allowed."):
        self.message = message
        super().__init__(self.message)

class StaticResourceUsageOutsideHeadError(Exception):
    """
    Raised when a static resource is tried to include outside the head term of a PyHTML file.
    """
    def __init__(self, message="Static resource usage out of <head> term detected."):
        self.message = message
        super().__init__(self.message)

class BooleanAlreadyTrueError(Exception):
    """
    Raised when trying to set a boolean that is already True.
    """
    def __init__(self, message="Boolean value is already True."):
        self.message = message
        super().__init__(self.message)#

class BetaAlreadyEnabledError(BooleanAlreadyTrueError):
    """
    Raised when trying to enable beta mode that is already enabled.
    """
    def __init__(self, message="Beta mode is already enabled."):
        self.message = message
        super().__init__(self.message)

class AccessToTemplateForbidden(Exception):
    """
    Raised when trying to access a template that is not allowed.
    """
    def __init__(self, message="Access to this template is forbidden."):
        self.message = message
        super().__init__(self.message)

class BetaAlreadyLocked(Exception):
    """
    Raised when trying to activate BETA mode when it is already locked.
    """
    def __init__(self, message="BETA mode already locked"):
        self.message = message
        super().__init__(self.message)

class BetaNotEnabledError(Exception):
    """
    Raised when trying to use a BETA feature when BETA mode is not enabled.
    """
    def __init__(self, message="BETA mode is not enabled."):
        self.message = message
        super().__init__(self.message)

class VercelIncompabilityError(Exception):
    """
    Raised when trying to use Vercel hosting without enabling Vercel compatibility.
    """
    def __init__(self, message="Vercel compatibility is not enabled."):
        self.message = message
        super().__init__(self.message)

class OutdatedPyWSGIRefVersionError(Exception):
    """
    Raised when the PyWSGIRef version is outdated and does not support a requested feature.
    """
    def __init__(self, message="The PyWSGIRef version is outdated and does not support this feature."):
        self.message = message
        super().__init__(self.message)