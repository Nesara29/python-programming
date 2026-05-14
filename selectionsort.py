def selection_sort(arr):
    for i in range(len(arr)):
        min_index=i
        for j in range(i+1,len(arr)):
            if arr[j]<arr[min_index]:
                min_index=j
        arr[i],arr[min_index]=arr[min_index],arr[i]
        print(f"pass {i+1}:swapping {arr[min_index]} with {arr[i]}->{arr}")
    return arr
arr=[65,72,23,14,34]
print("original array",arr)
selection_sort(arr)
print("sorted array",arr)