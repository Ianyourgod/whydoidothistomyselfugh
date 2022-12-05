class Node:
    def __init__(self,type,value1=None,value2=None) -> None:
        self.type = type
        self.value1 = value1
        self.value2 = value2
    def __str__(self) -> str:
        if self.value1 and self.value2: return f"[{self.type}: {self.value1}, {self.value2}]"
        if self.value1: return f"[{self.type}: {self.value1}]"
        return f"[{self.type}]"

class CreateAst:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.i = 0
        self.current_token = self.tokens[0]
        