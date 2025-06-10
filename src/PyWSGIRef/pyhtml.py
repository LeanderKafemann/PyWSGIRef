from naturalsize import replStr, replStrPassage

from .defaults import HELLO_WORLD as DEFAULT
from .commons import *
from .exceptions import InvalidIncludePhraseFiletypeError, StaticResourceUsageOutsideHeadError
from .beta import BETA

class PyHTML:
    def __init__(self, html: str = DEFAULT):
        self.html = html
    def decode(self):
        """
        Decodes the HTML content.
        """
        self.html = self.html.strip()

        # common html beginning phrase
        if self.html.startswith("<{{evalPyHTML}}>"):
            self.html = START_REPLACE + self.html[16:]

        # common html ending phrase
        if self.html.endswith("<{{evalPyHTML}}>"):
            self.html = self.html[:-16] + END_REPLACE
        
        if BETA.value():
            # static ressources
            idx = self.html.find("<{{evalPyHTML-include: ")
            if idx != -1:
                idxEnd = self.html.find(" :include-}}>", idx)
                if idxEnd > self.html.find("</head>"):
                    raise StaticResourceUsageOutsideHeadError()
                setIn = ""
                for i in self.html[idx:idxEnd+12].split(":")[1].strip().split(","):
                    if i.endswith(".css"):
                        setIn += "\t\t<link rel='stylesheet' href='{}'/>\n".format(i)
                    elif i.endswith(".js"):
                        setIn += "\t\t<script src='{}'></script>\n".format(i)
                    elif i.endswith(".json"):
                        setIn += "\t\t<link rel='manifest' href='{}'/>\n".format(i)
                    else:
                        raise InvalidIncludePhraseFiletypeError()
                self.html = replStrPassage(idx, idxEnd+12, self.html, setIn)

            # PyWSGIRef's styling
            idx = self.html.find("<{{evalPyHTML-modernStyling: true}}>")
            if idx != -1:
                self.html = replStrPassage(idx, idx+35, self.html, MODERN_STYLING)

    def decoded(self) -> str:
        """
        Returns the decoded HTML content.
        """
        self.decode()
        return self.html