def fact(n):
    if n==1:
        print("=1")
        return 1
    print(f"{n} * {fact(n-1)}")
    return n*fact(n-1)
n=int(input("enter a element:"))
print(f"fact({n})")
result=fact(n)
exp="*".join(str(i)for i in range(n,0,-1))
print("="+exp)
print("="+str(result))
