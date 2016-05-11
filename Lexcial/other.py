#coding=utf8
class Stack:
    def __init__(self,size = 16):
        self.stack = []
        self.size = size
        self.top = -1
    def setSize(self, size):
        self.size = size
    def isEmpty(self):
        if self.top == -1:
            return True
        else:
            return False
    def isFull(self):
        if self.top +1 == self.size:
            return True
        else:
            return False
    def _top(self):
        if self.isEmpty():
            #return None
            raise Exception("StackIsEmpty")
        else:
            return self.stack[self.top]
    def push(self,obj):
        if self.isFull():
            raise Exception("StackOverFlow")
        else:
            self.stack.append(obj)
            self.top +=1
    def pop(self):
        if self.isEmpty():
            raise Exception("StackIsEmpty")
        else:
            self.top -= 1
            return self.stack.pop()
    def show(self):
        print(self.stack)
