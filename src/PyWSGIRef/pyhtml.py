import html
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
        self.context = None

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

    def _replace_eval_blocks(self):
        """
        Replaces eval replacement phrases with evaluated Python expressions.
        WARNING: This method uses eval, which can execute arbitrary code.
        """
        if self.context is None:
            self.context = {}
        for match in re.finditer(EVAL_BLOCK_PATTERN, self.html, re.DOTALL):
            idx, idxEnd = match.span()
            code = match.group(1).strip()
            try:
                # eval für Ausdrücke, exec für Statements
                result = str(eval(code, {}, self.context))
            except Exception as e:
                result = f"<b>EvalError: {e}</b>"
            self.html = self.html[:idx] + result + self.html[idxEnd:]

    def _replace_if_blocks(self, context=None):
        """
        Replaces with html code based on the evaluation of conditions in if blocks.
        """
        if context is None:
            context = {}
        # re.DOTALL für mehrzeilige Blöcke
        while True:
            match = re.search(IF_BLOCK_PATTERN, self.html, re.DOTALL)
            if not match:
                break
            condition = match.group(1).strip()
            if_content = match.group(2)
            else_content = match.group(5) if match.group(5) is not None else ""
            try:
                if eval(condition, {}, context):
                    replacement = if_content
                else:
                    replacement = else_content
            except Exception as e:
                replacement = f"<b>IfEvalError: {e}</b>"
            self.html = self.html[:match.start()] + replacement + self.html[match.end():]

    def decode(self):
        """
        Decodes the HTML content by replacing specific phrases and applying modern styling.
        """
        self.html = self.html.strip()
        self._replace_eval_phrase()
        self._replace_modern_styling()
        self._replace_script_blocks()
        self._replace_style_blocks()
        if BETA.value:
            self._replace_includes()
            self._replace_eval_blocks()
            self._replace_if_blocks()

    def decoded(self, cacheDecoded: bool = False) -> str:
        """
        Returns the decoded HTML content.
        """
        backup = self.html
        self.decode()
        _return = self.html
        if not cacheDecoded:
            self.html = backup
        return _return

    def decodedContext(self, context: dict, cacheDecoded: bool = False) -> str:
        """
        Returns the decoded HTML content with the provided context.
        """
        self.context = context
        return self.decoded(cacheDecoded)