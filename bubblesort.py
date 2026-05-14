import time
def bubble_sort(arr):
    n=len(arr)
    print("Bubble sort steps")
    for i in range(n-1):
        print(f"pass,{i+1}")
        for j in range(n-i-1):
            if arr[j]>arr[j+1]:
                print(f"swapping {arr[j]} with {arr[j+1]}")
                arr[j],arr[j+1]=arr[j+1],arr[j]
        print(f" original array:{arr}")
        print(f" array after the pass:{i+1}:{arr}")
arr=[76,54,24,14,9]
print("original array:",arr)
start_time =time.perf_counter()
bubble_sort(arr)
end_time =time.perf_counter()
print("\n sorted array:" ,arr)
print("elapsed time:",end_time-start_time)

