def quicksort(arr):
    if len(arr)<=1:
        return arr
    pivot=arr[-1]
    left=[x for x in arr[:-1] if x<pivot]
    right=[x for x in arr[:-1] if x>pivot]
    print(f"pivot:{pivot},left:{left},right:{right}")
    print("pass:",left+[pivot]+right)
    return quicksort(left)+[pivot]+quicksort(right)
arr=[33,24,46,42,14,20]
print("original list:",arr)
arr=quicksort(arr)
print("sorted list:",arr)
