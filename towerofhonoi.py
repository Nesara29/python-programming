def hanoi(n,A,B,C,s,a,d):
    if n==0:
        return
    hanoi(n-1,A,C,B,s,d,a)
    disk=A.pop()
    C.append(disk)
    print(f"move disk {disk} from {s} to {d}")
    print(f"A:{A}|B:{B}|C:{C}\n")
    hanoi(n-1,B,A,C,a,s,d)
n=3
a_rod=[3,2,1]
b_rod=[]
c_rod=[]
print("initial states")
print(f"A:{a_rod}|B:{b_rod}|C:{c_rod}\n")
hanoi(n,a_rod,b_rod,c_rod,'A',"B","C")