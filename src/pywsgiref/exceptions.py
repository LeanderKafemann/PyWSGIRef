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