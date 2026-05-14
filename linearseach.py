import sys
import time

def linear_search(a,key):
    comparisons = 0
    for i in range(len(a)):
        comparisons += 1
        if a[i] == key:
            return i, comparisons
    return -1, comparisons

a = [10,20,30,40,50]
print(a)

key = int(input("enter number to search:"))
start_time = time.perf_counter()
start_space = sys.getsizeof(a)+sys.getsizeof(key)
result,comparisons = linear_search(a,key)
end_time = time.perf_counter()
end_space = sys.getsizeof(a)+sys.getsizeof(key)
print("---search result---")
if result != -1:
    print("key is found:", result)
else:
    print("key is not found")

if comparisons == 1:
    case = "best case"
elif comparisons == len(a):
    case = "worst case"
else:
    case = "average case"

print("case type:",case)
print("number of comparisons:",comparisons)
print("time taken:",end_time-start_time)
print("space taken:",end_space-start_space)





