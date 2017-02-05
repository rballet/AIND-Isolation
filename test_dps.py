graph = {'A': ['B','C','D'],
         'B': ['E','F','G'],
         'C': ['H','I','J'],
         'D': ['K','L','M'],
         'E': [],
         'F': [],
         'G': [],
         'H': [],
         'I': [],
         'J': [],
         'K': [],
         'L': [],
         'M': [],
         'N': [],
         'O': [],
         'P': [],}

def limited_dps(start, graph, max_depth, actual_depth=0):
    actual_depth += 1
    path = []
    if actual_depth >= max_depth or len(graph[start]) == 0:
        return [start]
#    if start == end:
#        return end
    if start not in graph:
        return False
    for node in graph[start]:
        path += limited_dps(node, graph, max_depth, actual_depth)
    return path
#        if path_temp:
#            path += path_temp
#            return path
            
            
print(limited_dps('A',graph,4))