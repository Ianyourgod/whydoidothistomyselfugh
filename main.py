class Function:
    def __init__(self,params,at,interpreter) -> None:
        self.params = params
        self.at = at
        self.interpreter = interpreter
        self.get_code()
    def parse_params(self):
        ret = []
        for i in self.params:
            if i == ",":
                continue
            ret.append(i)
        return ret
    def get_code(self):
        self.code = ""
        i = self.at
        open_parens = 1
        #print(self.interpreter.code)
        code = self.interpreter.getLines(self.interpreter.code)
        #print(code)
        while i < len(code):
            tokens = self.interpreter.tokenize(code[i])
            if "{" in tokens:
                open_parens += 1
            if "}" in tokens:
                open_parens -= 1
            if open_parens == 0:
                break
            self.code += code[i] + "\n"
            i += 1

class Interpreter:
    def __init__(self,code=None) -> None:
        self.vars = {}
        self.functions = {}
        self.function_stack = []
        self.line = 0
        self.open_brackets = 0
        self.code = code
    def getLines(self, code: str) -> list:
        ret = []
        txt = ""
        j = 0
        print(code)
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
        if code[0] in " \t":
            while code[0] in " \t":
                code = code[1:]
        while j < len(code):
            i = code[j]
            if i == None:
                print("ERROR: Unexpected none-type")
                return None
            elif i == " ":
                if txt != "":
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
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append("(")
            elif i == ")":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append(")")
            elif i == "[":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append("[")
            elif i == "]":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append("]")
            elif i == "{":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append("{")
            elif i == "}":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append("}")
            elif i == ",":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append(",")
            elif i == "+":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append("+")
            elif i == "-":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append("-")
            elif i == "*":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append("*")
            elif i == "/":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append("/")
            elif i == "%":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append("%")
            elif i == "^":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append("^")
            elif i == "&":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append("&")
            elif i == "|":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append("|")
            elif i == "!":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append("!")
            elif i == "<":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append("<")
            elif i == ">":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append(">")
            elif i == "?":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append("?")
            elif i == ".":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append(".")
            elif i == "=":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                if code[j+1] == "=":
                    tokens.append("==")
                    j += 1
                else:
                    tokens.append("=")
            elif i == "#":
                if txt != "":
                    tokens.append(txt)
                    txt = ""
                tokens.append("#")
            elif i.isnumeric():
                while j < len(code) and code[j].isnumeric():
                    txt += code[j]
                    j += 1
                j -= 1
            elif i.isalpha():
                while j < len(code) and (code[j].isalpha() or code[j].isnumeric()):
                    txt += code[j]
                    j += 1
                j -= 1
            else:
                txt += i
            j += 1
        if txt != "":
            tokens.append(txt)
        return tokens
    def runLine(self, line: str|list):
        if line is list:
                tokens = line
        else: tokens = self.tokenize(line)
        if (len(tokens) == 0):
            return
        self.line += 1
        if self.open_brackets < 1:
            # replaces all variables with their values
            j = 0
            while j < len(tokens):
                i = tokens[j]
                if i in self.vars and not (j == 0 and "=" in tokens):
                    tokens[j] = self.vars[i]
                j += 1
            if tokens[0] == "(":
                open_paren = 1
                for i in tokens:
                    if i == "(":
                        open_paren += 1
                    elif i == ")":
                        open_paren -= 1
                    if open_paren == 0:
                        break
                else:
                    print("ERROR: No closing parenthesis")
                    return "ERROR: No closing parenthesis"
            elif tokens[0] == "print":
                if len(tokens) > 1 and tokens[1] == "(":
                    if tokens[2] == ")":
                        print()
                    else:
                        innerTokens = tokens[2:-1]
                        print(self.runLine(innerTokens)[1:-1])
                else:
                    return("BUILTIN FUNCTION: print")
                return
            elif tokens[0] == "input":
                if tokens[1] == "(":
                    if tokens[2] == ")":
                        return input()
                    else:
                        innerTokens = tokens[2:-1]
                        return input(self.runLine(innerTokens))
                else:
                    return("BUILTIN FUNCTION: input")
                return
            elif tokens[0] == None:
                print("ERROR: unexpected none-type")
                return "ERROR: unexpected none-type"
            elif tokens[0].isnumeric():
                # create ast
                return self.runAST(tokens)
            elif self.isstring(tokens[0]):
                return self.string(tokens)
            elif tokens[0] == "let":
                if tokens[1] in self.vars:
                    print("ERROR: variable '" + tokens[1] + "' already exists")
                    return "ERROR: variable '" + tokens[1] + "' already exists"
                if len(tokens) > 2 and tokens[2] == "=":
                    self.vars[tokens[1]] = self.runLine(tokens[3:])
                else:
                    self.vars[tokens[1]] = None
            elif tokens[0] in self.vars:
                if tokens[1] in ["+","-", "*", "/", "%", "^","="]:
                    if tokens[1] == "=":
                        self.vars[tokens[0]] = self.runLine(tokens[2:])
                    elif tokens[2] == "=":
                        if tokens[1] == "+":
                            self.vars[tokens[0]] = self.vars[tokens[0]] + self.runLine(tokens[3:])
                        elif tokens[1] == "-":
                            self.vars[tokens[0]] = self.vars[tokens[0]] - self.runLine(tokens[3:])
                        elif tokens[1] == "*":
                            self.vars[tokens[0]] = self.vars[tokens[0]] * self.runLine(tokens[3:])
                        elif tokens[1] == "/":
                            self.vars[tokens[0]] = self.vars[tokens[0]] / self.runLine(tokens[3:])
                        elif tokens[1] == "%":
                            self.vars[tokens[0]] = self.vars[tokens[0]] % self.runLine(tokens[3:])
                        elif tokens[1] == "^":
                            self.vars[tokens[0]] = self.vars[tokens[0]] ** self.runLine(tokens[3:])
                    else:
                        self.vars[tokens[0]] = self.runLine(self.vars[tokens[0]] + tokens[1] + tokens[2])
            elif tokens[0] == "if":
                if self.runAST(tokens[1:-1]) == "True":
                    self.open_brackets -= 1
            elif tokens[0] == "#":
                return
            #elif tokens[0] == "func":
            #    if tokens[1] in self.funcs:
            #        print("ERROR: function '" + tokens[1] + "' already exists")
            #        return "ERROR: function '" + tokens[1] + "' already exists"
            #    j = 3
            #    params = []
            #    while tokens[j] != ")":
            #        params.append(tokens[j])
            #        j += 1
            #    self.funcs[tokens[1]] = Function(params, self.line+1)
            #elif tokens[0] in self.functions:
            #    if tokens[1] == "(":
            #        j = 2
            #        params = []
            #        while tokens[j] != ")":
            #            params.append(tokens[j])
            #            j += 1
            #        # get code
            #        linen = self.functions[tokens[0]].at
            elif "{" in tokens:
                pass
            elif "}" in tokens:
                pass
            else:
                print("ERROR: unknown identifier '" + tokens[0] + "'")
                return "ERROR: unknown identifier '" + tokens[0] + "'"
        if "{" in tokens:
            self.open_brackets += 1
        if "}" in tokens:
            if self.open_brackets == 0:
                self.open_brackets += 1
            self.open_brackets -= 1
            
            
    def runAST(self, tokens: list[str]) -> None:
        for i in tokens:
            if not ((i.isnumeric() or i in ["+", "-", "*", "/", "%", "^", "&", "|", "!", "<", ">", "?", ".", "==", "=","(",")"]) or self.isstring(i)):
                print(self.isstring(i))
                print(f"ERROR: expected number, got '{i}'")
                return f"ERROR: expected number, got '{i}'"
        return str(eval("".join(tokens)))
    def isstring(self, string: str) -> bool:
        if string[0] == '"' and string[-1] == '"':
            return True
        if string[0] == "'" and string[-1] == "'":
            return True
        return False
    def string(self, tokens: list) -> str:
        final = ""
        j = 0
        if self.isstring(tokens[0]):
            final += tokens[0][1:-1]
            j = 1
        while j < len(tokens):
            if tokens[j] == "+":
                j += 1
                if j > len(tokens):
                    print("ERROR: expected string after '+'")
                    return "ERROR: expected string after '+'"
                if self.isstring(tokens[j]):
                    final += tokens[j][1:-1]
                else:
                    print("ERROR: cannot add non-string to string")
                    return "ERROR: cannot add non-string to string"
            elif tokens[j] == "*":
                j += 1
                if j > len(tokens):
                    print("ERROR: expected number after '*'")
                    return "ERROR: expected number after '*'"
                if tokens[j].isnumeric():
                    final *= int(tokens[j])
                else:
                    print("ERROR: cannot multiply string by non-number")
                    return "ERROR: cannot multiply string by non-number"
            else:
                print("ERROR: expected '+' or '*' when concatenating strings")
                return "ERROR: expected '+' or '*' when concatenating strings"
            j += 1
        return f'"{final}"'
    def virtual_runner(self, lines: list[str], line) -> None:
        j = line - 1
        open_bracks = 1
        code = []
        while j < len(lines):
            tokens = self.tokenize(lines[j])
            if "{" in tokens:
                open_bracks += 1
            if "}" in tokens:
                open_bracks -= 1
            if open_bracks == 0:
                break
            code.append(lines[j])
            j += 1
        virtual_inter = Interpreter()
        virtual_inter.vars = self.vars
        virtual_inter.functions = self.functions
    def run(self,code: str) -> None:
        print(code)
        lines = self.getLines(code)
        self.line = 0
        print(lines)
        while self.line < len(lines):
            self.runLine(lines[self.line])
            self.line += 1
        
if __name__ == "__main__":
    inter = Interpreter()
    print(inter.runLine("print('hello world')"))