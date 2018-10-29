INTEGER,PLUS,MINUS,MUL,DIV,EOF = "integer","plus","minus","mul","div","eof"

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
        self.error()
        return Token(EOF,None)


class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self,token_type):
        if self.current_token.token_type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def error(self):
        raise Exception("error parsing text")

    def term(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def factor(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        #self.current_token = self.get_next_token()
        result = self.factor()
        while self.current_token.token_type in (MUL,DIV):
            token = self.current_token
            if token.token_type == MUL:
                self.eat(MUL)
                result *= self.factor()
            elif token.token_type == DIV:
                self.eat(DIV)
                result /= self.factor()
            else:
                self.error()
        return result

def main():
    while True:
        try:
            text = raw_input("calc>")
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print("result: {result}".format(result=result))

if __name__ == "__main__":
    main()

#you have a programming model,or know how to do something then write it from top to bottom
#before that, you may need to check for something

#python is really a bad language

#build a program and write corresponding test
