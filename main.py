import sys

class Error:
    def __init__(self, name, error, line):
        print(f"{name}: {error} at line {line}")
        sys.exit(1)

class Function:
    def __init__(self, args, line, interpreter):
        self.args = args
        self.line = line
        self.interpreter = interpreter
        self.get_code()
    def get_code(self):
        line = self.line
        self.code = ""
        open_brackets = 1
        while open_brackets > 0:
            line += 1
            if line >= len(self.interpreter.lines):
                Error("EOLError","Unexpected end of file",line)
                return None
            for i in self.interpreter.lines[line]:
                if i == "{":
                    open_brackets += 1
                elif i == "}":
                    open_brackets -= 1
            if open_brackets>0:self.code += self.interpreter.lines[line] + "\n"
        finline = ""
        for i in self.interpreter.lines[line]:
            if i == "}":
                break
            finline += i
        self.code += finline
        self.code = self.code[:-1]
                

class Interpreter:
    def __init__(self,code: str|list):
        self.line = 0
        self.code = code
        self.vars = {}
        self.funcs = {}
        self.func_stack = []
        if type(code) == str:self.lines = self.get_lines(code)
        else:self.lines = code
    def get_lines(self,code):
        lines = code.split("\n")
        i = 0
        ret = []
        while i < len(lines):
            linee = ""
            j = 0
            line = lines[i]
            if len(line) == 0:
                i += 1
                continue
            while line[j] in " \t":
                j += 1
                if j < len(line):
                    break
            if line[j] == "#":
                i += 1
                continue
            while j < len(line):
                linee += line[j]
                j += 1
            ret.append(linee)
            i += 1
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
                Error("ENTError","Unexpected none-type",self.line)
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
    def run(self):
        tokens_list = []
        open_braks = []
        for i in self.lines:
            tokens_list.append(self.tokenize(i))
        for tokens in tokens_list:
            j = 0
            while j < len(tokens):
                i = tokens[j]
                if i in self.vars and not (j == 0 and "=" in tokens):
                    tokens[j] = self.vars[i]
                j += 1
                self.runLine(tokens)
    def isstring(self,txt: str):
        if txt[0] == '"':
            if txt[1] == '"' and txt[2] == '"':
                i = 3
                while i < len(txt):
                    if txt[i] == '"' and txt[i+1] == '"' and txt[i+2] == '"':
                        return True
                    i += 1
                return False
            else:
                i = 1
                while i < len(txt):
                    if txt[i] == '"':
                        return True
                    if txt[i] == "\n":
                        Error("EOLError", "End of line reached before string was closed", self.line)
                return False
        elif txt[0] == "'":
            if txt[1] == "'" and txt[2] == "'":
                i = 3
                while i < len(txt):
                    if txt[i] == "'" and txt[i+1] == "'" and txt[i+2] == "'":
                        return True
                    i += 1
                return False
            else:
                i = 1
                while i < len(txt):
                    if txt[i] == '"':
                        return True
                    if txt[i] == "\n":
                        Error("EOLError", "End of line reached before string was closed", self.line)
                return False
    def tostring(self,x):
        if self.isstring(x):
            return x
        return f'"{x}"'
    def tobool(self,x):
        if self.isstring(x) and x != '""' and x != "''" and x != '""""""' and x != "''''''":
            return "true"
        elif x.isnumeric() and x != "0":
            return "true"
        return "false"
    def runmath(self,tokens):
        pass
    def runLine(self,tokens: str|list):
        BUILTINS = {"print":lambda x: print(self.tostring(x)),"input":lambda x: input(x),"int":lambda x,b=10: int(x,b),"float":lambda x, b: float(x,b),"str":self.tostring,"bool":self.tobool}
        if type(tokens) == str:
            temp_inter = Interpreter(self.get_lines(tokens))
            return temp_inter.run()
        if len(tokens) == 0:
            return None
        if tokens[0] == "let":
            temp_code = tokens[2:]
            self.vars[tokens[1]] = self.runLine(temp_code)
            return None
        elif tokens[0] in BUILTINS:
            if tokens[1] == "(":
                j = 2
                inp1 = ""
                inp2 = ""
                st1 = []
                st2 = []
                while j < len(tokens) and tokens[j] != ")":
                    if tokens[j] == ",":
                        j += 1
                        while j < len(tokens) and tokens[j] != ")":
                            st2.append(tokens[j])
                            j += 1
                        break
                    else:st1.append(tokens[j])
                    j += 1
                inp1 = self.runLine(st1)
                inp2 = self.runLine(st2)
                if inp2:
                    return BUILTINS[tokens[0]](inp1,inp2)
                else:
                    return BUILTINS[tokens[0]](inp1)
            else:
                return f"BUILTIN: {tokens[0]}"
        elif tokens[0].isnumeric():
            return self.runmath(tokens)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1],"r") as f:
            code = f.read()
        i = Interpreter(code)
    else:
        Error("NFSError","No file specified",0)