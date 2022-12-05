class Interpreter:
    def __init__(self) -> None:
        self.vars = {}
        self.functions = {}
    def getLines(self, code: str) -> list:
        ret = []
        txt = ""
        j = 0
        while j < len(code):
            i = code[j]
            if i in " \t":
                while i in " \t" and j < len(code):
                    j += 1
                    i = code[j]
            if i == "\n":
                if txt != "":
                    ret.append(txt)
                txt = ""
            j += 1
        if txt != "":
            ret.append(txt)
        return ret
    def tokenize(self,code: str) -> list:
        tokens = []
        j = 0
        txt = ""
        while j < len(code):
            i = code[j]
            if i == " ":
                tokens.append(txt)
                txt = ""
            elif i == '"':
                txt += i
                j += 1
                i = code[j]
                while i != '"':
                    txt += i
                    j += 1
                    i = code[j]
                txt += i
            elif i == "'":
                txt += i
                j += 1
                i = code[j]
                while i != "'":
                    txt += i
                    j += 1
                    i = code[j]
                txt += i
            elif i == "(":
                tokens.append(txt)
                txt = ""
                tokens.append("(")
            elif i == ")":
                tokens.append(txt)
                txt = ""
                tokens.append(")")
            elif i == "[":
                tokens.append(txt)
                txt = ""
                tokens.append("[")
            elif i == "]":
                tokens.append(txt)
                txt = ""
                tokens.append("]")
            elif i == "{":
                tokens.append(txt)
                txt = ""
                tokens.append("{")
            elif i == "}":
                tokens.append(txt)
                txt = ""
                tokens.append("}")
            elif i == ",":
                tokens.append(txt)
                txt = ""
                tokens.append(",")
            elif i == ":":
                tokens.append(txt)
                txt = ""
                tokens.append(":")
            elif i == "=":
                tokens.append(txt)
                txt = ""
                tokens.append("=")
            elif i == "+":
                tokens.append(txt)
                txt = ""
                tokens.append("+")
            elif i == "-":
                tokens.append(txt)
                txt = ""
                tokens.append("-")
            elif i == "*":
                tokens.append(txt)
                txt = ""
                tokens.append("*")
            elif i == "/":
                tokens.append(txt)
                txt = ""
                tokens.append("/")
            elif i == "%":
                tokens.append(txt)
                txt = ""
                tokens.append("%")
            elif i == "^":
                tokens.append(txt)
                txt = ""
                tokens.append("^")
            elif i == "&":
                tokens.append(txt)
                txt = ""
                tokens.append("&")
            elif i == "|":
                tokens.append(txt)
                txt = ""
                tokens.append("|")
            elif i == "!":
                tokens.append(txt)
                txt = ""
                tokens.append("!")
            elif i == "<":
                tokens.append(txt)
                txt = ""
                tokens.append("<")
            elif i == ">":
                tokens.append(txt)
                txt = ""
                tokens.append(">")
            elif i == "?":
                tokens.append(txt)
                txt = ""
                tokens.append("?")
            elif i == ".":
                tokens.append(txt)
                txt = ""
                tokens.append(".")
            else:
                txt += i
            j += 1
        return tokens
    def runLine(self, line: str) -> None:
        tokens = self.tokenize(line)
        if (len(tokens) == 0):
            return
        # replaces all variables with their values
        j = 1
        while j < len(tokens):
            i = tokens[j]
            if i in self.vars:
                tokens[j] = self.vars[i]
            j += 1
        if tokens[0] == "print":
            if tokens[1] == "(":
                if tokens[2] == ")":
                    print()
                else:
                    innerTokens = tokens[2:-1]
                    print(self.runLine(innerTokens))
            else:
                print("BUILTIN FUNCTION: print")
            return
        if tokens[0] == "input":
            if tokens[1] == "(":
                if tokens[2] == ")":
                    return input()
                else:
                    innerTokens = tokens[2:-1]
                    return input(self.runLine(innerTokens))
            else:
                print("BUILTIN FUNCTION: input")
            return
        if tokens[0].isnumeric():
            # create ast
            return self.runAST(tokens)
            
                
inter = Interpreter()
print(inter.tokenize("print('hello world')"))