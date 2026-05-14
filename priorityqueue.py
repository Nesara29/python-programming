queue=[]
n=int(input("enter the number of elements"))
for i in range(n):
    data=int(input("enter the data"))
    priority=int(input("enter the priority"))
    queue.append((priority,data))
    print("\nqueue element")
for p,d in queue:
    print(d,"priority",p)
queue.sort()
item=queue.pop(0)
print("\nremoved item:",item[1])
print("\nqueue element")
for p,d in queue:
    print(d,"priority",p)
