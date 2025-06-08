from .defaults import HELLO_WORLD as DEFAULT
from .commons import *

class PyHTML:
    def __init__(self, html: str = DEFAULT):
        self.html = html
    def decode(self):
        """
        Decodes the HTML content.
        """
        self.html = self.html.strip()
        if self.html.startswith("<{{evalPyHTML}}>"):
            self.html = START_REPLACE + self.html[16:]

    def decoded(self) -> str:
        """
        Returns the decoded HTML content.
        """
        self.decode()
        return self.html