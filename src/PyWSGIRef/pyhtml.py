import re
from naturalsize import replStrPassage

from .defaults import HELLO_WORLD as DEFAULT
from .commons import *
from .exceptions import InvalidIncludePhraseFiletypeError, StaticResourceUsageOutsideHeadError
from .beta import BETA
from .patterns import *

class PyHTML:
    def __init__(self, html: str = DEFAULT):
        self.html = html

    def _replace_eval_phrase(self):
        """
        Scans the HTML for the evalPyHTML phrase and replaces it with the appropriate start and end phrases.
        """
        if self.html.startswith(EVAL_PYHTML):
            self.html = START_REPLACE + self.html[len(EVAL_PYHTML):]
        if self.html.endswith(EVAL_PYHTML):
            self.html = self.html[:-len(EVAL_PYHTML)] + END_REPLACE

    def _replace_modern_styling(self):
        """
        Scans the HTML for the modern styling phrase and replaces it with the appropriate CSS.
        """
        idx = self.html.find(MODERN_STYLING_PHRASE)
        if idx != -1:
            head_idx = self.html.find("</head>")
            if idx > head_idx:
                raise StaticResourceUsageOutsideHeadError()
            self.html = replStrPassage(idx, idx+len(MODERN_STYLING_PHRASE), self.html, MODERN_STYLING)

    def _replace_includes(self):
        """
        Scans the HTML for include phrases and replaces them with the appropriate resources.
        """
        for match in re.finditer(INCLUDE_PATTERN, self.html):
            idx, idxEnd = match.span()
            head_idx = self.html.find("</head>")
            if idx > head_idx:
                raise StaticResourceUsageOutsideHeadError()
            resources = match.group(1).split(",")
            setIn = ""
            for i in resources:
                i = i.strip()
                if i.endswith(".css"):
                    setIn += f"\t\t<link rel='stylesheet' href='{i}'/>\n"
                elif i.endswith(".js"):
                    setIn += f"\t\t<script src='{i}'></script>\n"
                elif i.endswith(".json"):
                    setIn += f"\t\t<link rel='manifest' href='{i}'/>\n"
                elif i.endswith("favicon.ico"):
                    setIn += f"\t\t<link rel='icon' href='{i}'/>\n"
                else:
                    raise InvalidIncludePhraseFiletypeError()
            self.html = self.html[:idx] + setIn + self.html[idxEnd:]

    def _replace_script_blocks(self):
        """
        Replaces script replacement phrases with JS scripts.
        """
        for match in re.finditer(SCRIPT_PATTERN, self.html, re.DOTALL):
            idx, idxEnd = match.span()
            script_content = match.group(1).strip()
            replacement = f"<script>{script_content}</script>"
            self.html = self.html[:idx] + replacement + self.html[idxEnd:]

    def _replace_style_blocks(self):
        """
        Replaces style replacement phrases with CSS styles.
        """
        for match in re.finditer(STYLE_PATTERN, self.html, re.DOTALL):
            idx, idxEnd = match.span()
            style_content = match.group(1).strip()
            replacement = f"<style>{style_content}</style>"
            self.html = self.html[:idx] + replacement + self.html[idxEnd:]

    def decode(self):
        """
        Decodes the HTML content by replacing specific phrases and applying modern styling.
        """
        self.html = self.html.strip()
        self._replace_eval_phrase()
        self._replace_modern_styling()
        if BETA.value:
            self._replace_includes()
            self._replace_script_blocks()
            self._replace_style_blocks()

    def decoded(self) -> str:
        """
        Returns the decoded HTML content.
        """
        self.decode()
        return self.html