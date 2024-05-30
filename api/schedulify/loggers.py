import logging

import pygments
import sqlparse

from pygments.formatters.terminal256 import TerminalTrueColorFormatter
from pygments.lexers import find_lexer_class_by_name


SqlLexer = find_lexer_class_by_name("sql")


class SQLFormatter(logging.Formatter):
    def format(self, record):
        sql = sqlparse.format(record.sql.strip(), reindent=True)
        record.statement = pygments.highlight(sql, SqlLexer(), TerminalTrueColorFormatter(style="monokai"))
        return super().format(record)
