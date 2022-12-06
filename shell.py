import main

if __name__ == "__main__":
    inter = main.Interpreter()
    while True:
        try:
            code = input(">>> ")
            if code == "exit()":
                break
            ret = inter.runLine(code)
            if ret:
                print(ret)
        except KeyboardInterrupt:
            break