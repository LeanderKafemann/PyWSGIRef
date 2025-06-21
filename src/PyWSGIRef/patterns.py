EVAL_PYHTML = "<{{evalPyHTML}}>"

MODERN_STYLING_PHRASE = "<{{evalPyHTML-modernStyling: true}}>"

INCLUDE_PATTERN = r"<\{\{evalPyHTML-include: (.*?) :include-\}\}\>"

SCRIPT_PATTERN = r"<\{\{evalPyHTML-script: (.*?) :script-\}\}\>"

STYLE_PATTERN = r"<\{\{evalPyHTML-style: (.*?) :style-\}\}\>"

EVAL_BLOCK_PATTERN = r"<\{\{evalPyHTML-eval: (.*?) :eval-\}\}\>"

IF_BLOCK_PATTERN = r"<\{\{evalPyHTML-if: (.*?)\}\}\>(.*?)((<\{\{evalPyHTML-else\}\}\>(.*?))?)<\{\{evalPyHTML-endif\}\}\>"