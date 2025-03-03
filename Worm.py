from BaseFunction import global_symbol_table
from Constants import *
from Context import *
from Error import *
from Error_Pointer_Arrow import *
from Interpreter import *
from Lexer import *
from Nodes import *
from Parser import *
from Position import *
from RunTime import *
from Token import *
from Value import *
import string
import re

def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    # Run program
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
