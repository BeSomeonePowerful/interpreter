INTEGER,PLUS,EOF = "integer","plus","eof"

class Token:
    def __init__(self,token_type,value):
        self.token_type = token_type
        self.value = value
    def __str__(self):
        return "Token:{token_type},{value}".format(token_type=self.token_type,value=self.value)
    def __repr__(self):
        return self.__str__()

class Interpreter:
    def __init__(self,text):
        self.text = text
        self.pos = 0
        self.current_token = None

    def error(self):
        raise Exception("error parsing text")

    def get_next_token(self):
        text = self.text
        if self.pos > len(text) -1 :
            return Token(EOF,None)
        current_char = text[self.pos]
        self.pos += 1
        if current_char.isdigit():
            return Token(INTEGER,current_char)
        if current_char == '+':
            return Token(PLUS,current_char)
        self.error()

    def eat(self,token_type):
        if self.current_token.token_type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()
        left = self.current_token
        self.eat(INTEGER)   #compare and move to next token
        self.eat(PLUS)
        right = self.current_token
        self.eat(INTEGER)
        result = left.value + right.value
        return result

def main():
    while True:
        try:
            text = raw_input("calc>")
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print("result: {result}".format(result=result))

if __name__ == "__main__":
    main()

#you have a programming model,or know how to do something then write it from top to bottom
#before that, you may need to check for something

#python is really a bad language
