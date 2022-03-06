#!/usr/bin/env python

"""
This script compares the median execution duration of 2 implementations of the BFS:
- A naive version using only regular lists as data structures
- An improved version where... (TODO)

Both implementation are executed 10 times and we compare the median of their execution time rounded to 4 digits.

We represent a graph as a dictionary in the form {parent: [children]}, for example:
graph = {
  0: [4, 1],
  1: [],
  2: [2, 3],
  3: [5, 6, 2],
  4: [7]
}

"""

def bfs_naive(graph, root=1):
    visited = [root]
    queue = [root]
    while len(queue) > 0:
        node = queue.pop(0)
        for child in graph[node]:
            if child not in visited:
                queue.append(child)
                visited.append(child)

def bfs_improved(graph, root=1):
    raise NotImplementedError("You must implement 'bfs_improved' as an improved version of 'bfs_naive'")
    # TODO

def generate_graph(n:int):
    """
    Generates a sample graph made of random nodes and leaves.
    """
    from random import randint, choice
    return {k: [randint(1, n-1) for _ in range(randint(0, n//3))] for k in range(n)}

from timeit import Timer
from statistics import median

graph = generate_graph(1000)
naive_time = median(Timer("bfs_naive(graph)", globals=globals()).repeat(repeat=10, number=1))
improved_time = median(Timer("bfs_improved(graph)", globals=globals()).repeat(repeat=10, number=1))

print(f"Naive BFS: exec time = {naive_time:.4f} secs")
print(f"Improved BFS: exec time = {improved_time:.4f} secs")
