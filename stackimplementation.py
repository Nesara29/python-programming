class stack:
    def __init__(self,limit):
        self.stack=[]
        self.size=0
        self.limit=limit
    def push(self,x):
        if self.size == self.limit:
            print("stack overflow")
            return
        self.stack.append(x)
        self.size += 1
        print(x,"pushed")
    def pop(self):
        if self.size == 0:
            print("stack underflow")
            return
        print(self.stack.pop(),"removed")
        self.size -= 1

    def display(self):
        if self.size == 0:
            print("stack empty")
            return
        for i in reversed(self.stack):
            print(i)
s=stack(3)
s.push(1)
s.push(2)
s.push(3)
s.push(4)
s.display()
s.pop()
s.pop()
s.pop()
s.pop()


