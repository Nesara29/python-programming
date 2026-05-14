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
def dfs(n):
    if n not in visited:
        print(n,end="->")
        visited.append(n)
        for i in graph[n]:
            dfs(i)
dfs(50)
