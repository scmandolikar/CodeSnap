# codesnap/core/syntax_highlighter.py

from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from pygments import highlight
from pygments.lexers import get_lexer_by_name
# This is the corrected line:
from pygments.formatter import Formatter 
from pygments.styles import get_style_by_name

class PygmentsFormatter(Formatter):
    """A custom Pygments formatter to interface with QSyntaxHighlighter."""
    def __init__(self):
        super().__init__()
        self.data = []

    def format(self, tokensource, outfile):
        # outfile is not used in this implementation
        self.data.clear()
        for ttype, value in tokensource:
            self.data.append((ttype, value))

class SyntaxHighlighter(QSyntaxHighlighter):
    """QSyntaxHighlighter that uses Pygments to style text."""
    def __init__(self, parent, language='python', style='monokai'):
        super().__init__(parent)
        self.formatter = PygmentsFormatter()
        try:
            self.lexer = get_lexer_by_name(language)
        except:
            self.lexer = get_lexer_by_name('text') # Fallback

        self.style = get_style_by_name(style)
        self.formats = {}
        for token, s in self.style:
            fmt = QTextCharFormat()
            if s['color']:
                fmt.setForeground(QColor(f"#{s['color']}"))
            if s['bgcolor']:
                fmt.setBackground(QColor(f"#{s['bgcolor']}"))
            if s['bold']:
                fmt.setFontWeight(QFont.Weight.Bold)
            if s['italic']:
                fmt.setFontItalic(True)
            if s['underline']:
                fmt.setFontUnderline(True)
            self.formats[token] = fmt

    def set_language(self, language):
        try:
            self.lexer = get_lexer_by_name(language)
        except:
            self.lexer = get_lexer_by_name('text')
        self.rehighlight()

    def highlightBlock(self, text):
        if not text:
            return
        # The highlight function writes to the formatter's outfile,
        # but our custom format method just populates self.formatter.data
        highlight(text, self.lexer, self.formatter)
        
        start = 0
        for ttype, value in self.formatter.data:
            length = len(value)
            self.setFormat(start, length, self.formats.get(ttype, QTextCharFormat()))
            start += length