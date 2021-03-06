import re


ID = 'ID'
AND = 'AND'
ADD = 'ADD'
ARRAY = 'ARRAY'
ASSIGN = 'ASSIGN'
ASEQ = 'ASEQ'
BAND = 'BAND'
BREAK = 'BREAK'
BEGIN = 'BEGIN'
BOOL = 'BOOL'
BOOLEAN = 'BOOLEAN'
BOR = 'BOR'
CHAR = 'CHAR'
CHARACTER = 'CHARACTER'
CONTINUE = 'CONTINUE'
COLON = 'COLON'
DIVIDE = 'DIVIDE'
DO = 'DO'
ELSE = 'ELSE'
EQ = 'EQ'
END = 'END'
EOF = '$'
FUNCTION = 'FUNCTION'
FALSE = 'FALSE'
LBRA = 'LBRA'
LES = 'LES'
LEQ = 'LEQ'
MULTIPLY = 'MULTIPLY'
NEQ = 'NEQ'
INT = 'INT'
REA = 'REA'
OR = 'OR'
GRE = 'GRE'
GEQ = 'GEQ'
LNOT = 'LNOT'
MOD = 'MOD'
PROCEDURE = 'PROCEDURE'
IF = 'IF'
INTEGER = 'INTEGER'
OF = 'OF'
RBRA = 'RBRA'
READ = 'READ'
REAL = 'REAL'
RETURN = 'RETURN'
RPAR = 'RPAR'
MINUS = 'MINUS'
SEMICOLON = 'SEMICOLON'
SINGLE_LINE_COMMENT = 'SINGLE_LINE_COMMENT'
MULTI_LINE_COMMENT_START = 'MULTI_LINE_COMMENT_START'
MULTI_LINE_COMMENT_END = 'MULTI_LINE_COMMENT_END'
STRING = 'STRING'
STR = 'STR'
XOR = 'XOR'
VAR = 'VAR'
THEN = 'THEN'
TRUE = 'TRUE'
WHILE = 'WHILE'
WRITE = 'WRITE'
LPAR = 'LPAR'
WHITESPACE = 'WHITESPACE'

regex_es = [
    (ADD, '^[+]$'),
    (AND, '^and$'),
    (ASEQ, '^(:=)$'),
    (ARRAY, '^array$'),
    (ASSIGN, '^assign$'),
    (BAND, '^[&]$'),
    (BOOL, '^(true)$|^(false)$'),
    (BOOLEAN, '^boolean$'),
    (BOR, '^[|]$'),
    (BREAK, '^break$'),
    (BEGIN, '^begin$'),
    (CHAR, '^char$'),
    (CONTINUE, '^continue$'),
    (COLON, '^[:]$'),
    (DIVIDE, '^[/]$'),
    (DO, '^do$'),
    (ELSE, '^else$'),
    (EQ, '^(=)$'),
    (END, '^end$'),
    (EOF, '^[$]$'),
    (FALSE, '^false$'),
    (FUNCTION, '^function$'),
    (LBRA, '^[[]$'),
    (LPAR, '^[(]$'),
    (MOD, '^[%]$'),
    (MULTIPLY, '^[*]$'),
    (NEQ, '^(<>)$'),
    (OR, '^or$'),
    (LES, '^[<]$'),
    (LEQ, '^[<=]$'),
    (GRE, '^[>]$'),
    (GEQ, '^[>=]$'),
    (LNOT, '^[~]$'),
    (MINUS, '^[-]$'),
    (PROCEDURE, '^procedure$'),
    (RPAR, '^[)]$'),
    (SINGLE_LINE_COMMENT, '^//$|^--$'),
    (MULTI_LINE_COMMENT_START, '^<--$'),
    ('MLC1', '^<-$'),
    ('MLC2', '^--$'),
    (MULTI_LINE_COMMENT_END, '^-->$'),
    (INTEGER, '^integer$'),
    (IF, '^if$'),
    (OF, '^of$'),
    (RBRA, '^[]]$'),
    (READ, '^read$'),
    (RETURN, '^return$'),
    (REAL, '^real$'),
    (SEMICOLON, '^[;]$'),
    (STRING, '^string$'),
    (THEN, '^then$'),
    (TRUE, '^true$'),
    (WHILE, '^while$'),
    (WHITESPACE, '\n|\t|\f|\r|\v|\s'),
    (WRITE, '^write$'),
    (VAR, '^var$'),
    (XOR, '^[\^]$'),
    (ID, '^([a-zA-Z])\w*$'),
    (INT, '^([0-9])+$'),
    (REA, '^([0-9])+[.]([0-9])*$')
]


class Token:
    def __init__(self, type=None, value=None):
        self.type = type
        self.value = value


class Scanner:

    def __init__(self, file):
        self.text = file.read()
        self.text += ' $'
        self.pointer = 0
        self.text_enum = list(self.text)
        # print(self.text_enum)

        while re.match('\n|\t|\f|\r|\v|\s', self.text_enum[self.pointer]):
            self.pointer += 1

    def parseToken(self):

        token_text = ""
        token = Token()
        while re.match('\n|\t|\f|\r|\v|\s', self.text_enum[self.pointer]):
            self.pointer += 1

        if self.text_enum[self.pointer] == "'":
            if self.text_enum[self.pointer + 2] != "'":
                return Token(None, None)
            token.type = CHARACTER
            token.value = self.text_enum[self.pointer + 1]
            self.pointer += 3
            return token

        if self.text_enum[self.pointer] == '"':
            token.type = STR
            self.pointer += 1
            while self.text_enum[self.pointer] != '"':
                token_text += self.text_enum[self.pointer]
                self.pointer += 1
            self.pointer += 1
            token.value = token_text
            return token
        if re.match('\n|\t|\f|\r|\v|\s', self.text_enum[self.pointer]):
            pass
            #print(True)

        while not re.match('\n|\t|\f|\r|\v|\s', self.text_enum[self.pointer]):
            token_text += self.text_enum[self.pointer]
            if re.match('^//$', token_text):
                while self.text_enum[self.pointer] != '\n':
                    self.pointer += 1
                while re.match('\n|\t|\f|\r|\v|\s', self.text_enum[self.pointer]):
                    self.pointer += 1
                token = Token()
                token_text = ''
                continue
            if re.match('^--$', token_text):
                if self.text_enum[self.pointer + 1] != '>':
                    while self.text_enum[self.pointer] != '\n':
                        self.pointer += 1
                    while re.match('\n|\t|\f|\r|\v|\s', self.text_enum[self.pointer]):
                        self.pointer += 1
                    token = Token()
                    token_text = ''
                    continue
            if re.match('^<--$', token_text):
                self.pointer += 1
                com_token = self.parseToken()
                while com_token.type != MULTI_LINE_COMMENT_END:
                    com_token = self.parseToken()
                while re.match('\n|\t|\f|\r|\v|\s', self.text_enum[self.pointer]):
                    self.pointer += 1
                token = Token()
                token_text = ''
                continue
            changed = False
            new_token_type = token.type
            new_token_values = token.value
            i = 0
            for t in regex_es:
                i +=1
                # print(t[1], i)
                if re.match(t[1], token_text):
                    new_token_type = t[0]
                    new_token_values = token_text
                    changed = True
                    break
            if not changed:

                return token
            else:
                token.type = new_token_type
                token.value = new_token_values
            if token.type == EOF:
                break
            self.pointer += 1
        return token