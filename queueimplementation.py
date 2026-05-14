class queue:
    def __init__(self,limit):
        self.queue=[]
        self.limit=limit
    def enqueue(self,x):
        if len(self.queue)==self.limit:
            print("queue overflow")
            return
        self.queue.append(x)
        print(x,"inserted")
    def dequeue(self):
        if len(self.queue)==0:
            print("queue underflow")
            return
        print(self.queue.pop(0),"removed")
    def display(self):
        if len(self.queue)==0:
            print("queue underflow")
            return
        for i in self.queue:
            print(i)
q=queue(3)
q.enqueue(1)
q.enqueue(2)
q.enqueue(3)
q.enqueue(4)
q.display()
q.dequeue()
q.dequeue()
q.dequeue()
q.dequeue()









