import main
from sys import argv

inter = main.Interpreter("""
print("running")
# def main() 
    print("hello world")
#
""")

func = main.Function("",1,inter)
#print(func.code)

if __name__ == "notmain":
    with open(argv[1], "r") as f:
        inter = main.Interpreter()
        code = f.read()
        inter.run(code)