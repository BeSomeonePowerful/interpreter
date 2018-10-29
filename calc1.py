INTEGER,PLUS,MINUS,MUL,DIV,LPAREN,RPAREN,EOF,EXIT = "integer","plus","minus","mul","div","(",")","eof","EXIT"

class Token:
    def __init__(self,token_type,value):
        self.token_type = token_type
        self.value = value
    def __str__(self):
        return "Token:{token_type},{value}".format(token_type=self.token_type,value=self.value)
    def __repr__(self):
        return self.__str__()

class Lexer:
    def __init__(self,text):
        self.text = text
        self.pos = 0
        #self.current_token = None
        self.current_char = self.text[self.pos]


    def integer(self):
        #skip whitespace and get integer
        value = ""
        while self.current_char is not None and self.current_char.isdigit():
            value = value + self.current_char
            self.advance()
        return int(value)


    #advance move both pos and current_char
    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
        if self.current_char is None:
            return Token(EOF, None)
        if self.current_char.isdigit():
            return Token(INTEGER,self.integer())
        if self.current_char == "+":
            self.advance()
            return Token(PLUS,"+")
        if self.current_char == "-":
            self.advance()
            return Token(MINUS,"-")
        if self.current_char == "*":
            self.advance()
            return Token(MUL,"*")
        if self.current_char == "/":
            self.advance()
            return Token(DIV,"/")
        if self.current_char == "(":
            self.advance()
            return Token(LPAREN,"(")
        if self.current_char == ")":
            self.advance()
            return Token(RPAREN,")")
        self.error()
        return Token(EOF,None)

class AST(object):
    pass

class BinOp(AST):
    def __init__(self,left,op,right):
        self.left = left
        self.op = op
        self.right = right

class Num(AST):
    def __init__(self,token):
        self.token = token
        self.value = self.token.value

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self,token_type):
        #print("current_token: %s,token_type: %s" % (self.current_token.token_type,token_type))
        if self.current_token.token_type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def error(self):
        raise Exception("error parsing text")

    #expr: term (+|- term)*
    #term: factor (*|/ factor)*
    #factor: integer
    def term(self):
        node = self.factor()
        while self.current_token.token_type in (MUL,DIV):
            # token = self.current_token
            # if token.token_type == MUL:
            #     self.eat(MUL)
            #     result = result * self.factor()
            # elif token.token_type == DIV:
            #     self.eat(DIV)
            #     result = result / self.factor()
            # else:
            #     self.error()
            token = self.current_token
            if token.token_type == MUL:
                self.eat(MUL)
            elif token.token_type == DIV:
                self.eat(DIV)
            else:
                self.error()
            node = BinOp(node,token,self.factor())
        return node

        return result

    def factor(self):
        token = self.current_token
        if token.token_type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.token_type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            self.error()

    def expr(self):
        #self.current_token = self.get_next_token()
        node = self.term()
        while self.current_token.token_type in (PLUS,MINUS):
            token = self.current_token
            # if token.token_type == PLUS:
            #     self.eat(PLUS)
            #     result += self.term()
            # elif token.token_type == MINUS:
            #     self.eat(MINUS)
            #     result -= self.term()
            # else:
            #     self.error()
            if token.token_type == PLUS:
                self.eat(PLUS)
            elif token.token_type == MINUS:
                self.eat(MINUS)
            else:
                self.error()
            node = BinOp(node,token,self.term())
        return node

class NodeVisitor:
    def visit(self,node):
        method_name = "visit_" + type(node).__name__
        #print("visiting [%s]" % type(node).__name__)
        visitor = getattr(self,method_name,self.generic_visit)
        return visitor(node)

    def generic_visit(self,node):
        raise Exception("visit of %s not implemented" % type(node).__name__)

class Interpreter(NodeVisitor):
    def __init__(self,parser):
        self.parser = parser

    def visit_BinOp(self,node):
        leftValue = self.visit(node.left)
        rightValue = self.visit(node.right)
        if node.op.token_type == PLUS:
            return leftValue + rightValue
        elif node.op.token_type == MINUS:
            return leftValue - rightValue
        elif node.op.token_type == MUL:
            return leftValue * rightValue
        elif node.op.token_type == DIV:
            return leftValue / rightValue

    def visit_Num(self,node):
        return node.value

    def interpret(self):
        node = self.parser.expr()
        return self.visit(node)

def main():
    while True:
        try:
            text = raw_input("calc>")
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print("result: {result}".format(result=result))

if __name__ == "__main__":
    main()

#support nested function call
#support compound data type
#you have a programming model,or know how to do something then write it from top to bottom
#before that, you may need to check for something

#python is really a bad language

#build a program and write corresponding test
