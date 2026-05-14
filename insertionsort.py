arr=[7,3,5,4,2,]
print("phases:Sorted|Unsorted")
for i in range(1,len(arr)):
    key=arr[i]
    j=i-1
    while j>=0 and arr[j]>key:
        arr[j+1]=arr[j]
        j-=1
    arr[j+1]=key
    print(f"pass:{i}",arr[:i+1],"|",arr[i+1:])
print("sorted array",arr)
