import string
DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

#######################################
# TOKENS
#######################################

WORM_INT = 'INT'
WORM_STRING = 'STRING'
WORM_IDENTIFIER = 'IDENTIFIER'
WORM_KEYWORD = 'KEYWORD'
WORM_PLUS = 'PLUS'
WORM_MINUS = 'MINUS'
WORM_MUL = 'MUL'
WORM_DIV = 'DIV'
WORM_MOD = 'MOD'
WORM_POW = 'POW'
WORM_EQ = 'EQ'
WORM_LPAREN = 'LPAREN'
WORM_RPAREN = 'RPAREN'
WORM_EE = 'EE'
WORM_NE = 'NE'
WORM_LT = 'LT'
WORM_GT = 'GT'
WORM_LTE = 'LTE'
WORM_GTE = 'GTE'
WORM_COMMA = 'COMMA'
WORM_COLON = 'COLON'
WORM_NEWLINE = 'NEWLINE'
WORM_EOF = 'EOF'

KEYWORDS = [
    'AND',
    'OR',
    'NOT',
    'IF',
    'ELIF',
    'ELSE',
    'FOR',
    'TO',
    'STEP',
    'LET',
    'THEN',
    'END',
    'RETURN',
    'CONTINUE',
    'BREAK',
    'LAMBDA'
]


