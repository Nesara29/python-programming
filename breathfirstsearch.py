graph={
    50:[30,70],
    30:[20,40],
    70:[60,80],
    20:[],
    40:[],
    60:[],
    80:[]
}
visited=[]
queue=[]
def bsf(start):
    visited.append(start)
    queue.append(start)
    while queue:
        node=queue.pop(0)
        print(node,end="->")
        for n in graph[node]:
            if n not in visited:
                visited.append(n)
                queue.append(n)
bsf(50)

