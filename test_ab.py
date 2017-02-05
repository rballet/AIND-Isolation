''' Example obtained from AIMA (2nd Ed.) Fig. 6.5 - 6.7 '''
import operator
import timeit

graph = {'A': ['B','C','D'],
         'B': ['E','F','G'],
         'C': ['H','I','J'],
         'D': ['K','L','M'],
         'E': 3,
         'F': 12,
         'G': 8,
         'H': 2,
         'I': 4,
         'J': 6,
         'K': 14,
         'L': 5,
         'M': 2,}
         
def alphabeta(graph, node='A', alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
    ''' Input: graph, alpha, beta, flag; Output: value, best_node '''
    print(node,alpha,beta,maximizing_player)
    input("Enter")
    if not isinstance(graph[node], list):
        return graph[node], node
    
    # Set upper/lower bound for value
    if maximizing_player:
        # Lower bound
        value = -float("inf")
    else:
        # Upper bound
        value = float("inf")
    
    best_node = graph[node][0]
    
    for move in graph[node]:
        if maximizing_player:
            print("MAX: ",node,alpha,beta,move)
            input("Enter")
            result, _ = alphabeta(graph, move, alpha, beta, maximizing_player=False)
            print("MAX: ",node,move,value,alpha,beta,best_node,result)
            value, best_node = max((value, best_node), (result, move))
            print("MAX: ",node,move,value,alpha,beta,best_node,result)
            input("Enter")
            if value >= beta:
                break
            alpha = max(alpha, value)
            print("MAX: ",node,move,value,alpha,beta,best_node,result)
            input("Enter")
        else:
            print("MIN: ",node,alpha,beta,move)
            input("Enter")
            result, _ = alphabeta(graph, move, alpha, beta, maximizing_player=True)
            print("MIN: ",node,move,value,alpha,beta,best_node,result)
            value, best_node = min((value, best_node), (result, move))
            print("MIN: ",node,move,value,alpha,beta,best_node,result)
            input("Enter")
            if value <= alpha:
                break
            beta = min(beta, value)
            print("MIN: ",node,move,value,alpha,beta,best_node,result)
            input("Enter")
    return value, best_node
    
#print("Result: ", alphabeta(graph))

lis=[(840, 32), (841, 3), (842, 4), (843, 4), (844, 6), (845, 6), (846, 12), (847, 6), (848, 10), (848, 12)]

timeit.timeit('max(lis,key=itemgetter(0))',number = 10000)
timeit.timeit('max(lis)',number = 10000)
#print(max(lis, key=operator.itemgetter(0)))