graph = {
  '5' : ['3','7', '9'],
  '3' : ['2', '4', '10'],
  '7' : ['8'],
  '2' : [],
  '4' : ['8', '9'],
  '8' : [],
  '9' : ['13','12', '11'],
  '10': ['13', '11', '8', '9'],
  '11': ['3','7', '9'],
  '12': [],
  '13': []
}

def bfs_with_queue(graph, root='5') -> list:
    from collections import deque

    visited = [root]
    queue = deque([root])
    while len(queue) > 0:
        node = queue.popleft()
        for child in graph[node]:
            if child not in visited:
                queue.append(child)
                visited.append(child)


def bfs_naive(graph, root='5') -> list:
    visited = [root]
    queue = [root]
    while len(queue) > 0:
        node = queue.pop(0)
        for child in graph[node]:
            if child not in visited:
                queue.append(child)
                visited.append(child)

from timeit import Timer
print(Timer("bfs_naive(graph)", globals=globals()).repeat())
#print(Timer("bfs_with_queue(graph)", globals=globals()).repeat())

def generate_graph(n:int):
    from random import randint, choice
    return {k: [randint(1, n-1) for _ in range(randint(0, n//3))] for k in range(n)}

# bfs_naive(generate_graph(10000), root=1)