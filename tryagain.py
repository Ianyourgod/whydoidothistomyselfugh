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
                print("ERROR: Unexpected end of file")
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
    def __init__(self,code):
        self.line = 0
        self.code = code
        self.vars = {}
        self.funcs = {}
        self.func_stack = []
        self.lines = self.get_lines(code)
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


inter = Interpreter("""def test() {
print("Hello World!")
}""")
func = Function("",0,inter)
print(func.code)