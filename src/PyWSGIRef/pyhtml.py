from .defaults import HELLO_WORLD as DEFAULT

class PyHTML:
    def __init__(self, html: str = DEFAULT):
        self.html = html
    def decode(self):
        """
        Decodes the HTML content.
        """
        self.html = self.html.strip()
    def decoded(self) -> str:
        """
        Returns the decoded HTML content.
        """
        self.decode()
        return self.html