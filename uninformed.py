from collections import deque
import heapq

# 1. Breadth-First Search (BFS)
def bfs(graph, start, goal):
    queue = deque([[start]])
    visited = set()
    expanded_count = 0
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        
        if node == goal:
            cost = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
            return path, round(cost, 2), expanded_count
            
        if node not in visited:
            visited.add(node)
            expanded_count += 1
            for neighbor in graph.get(node, {}):
                if neighbor not in visited:
                    queue.append(path + [neighbor])
    return None, 0, expanded_count

# 2. Depth-First Search (DFS)
def dfs(graph, start, goal):
    stack = [[start]]
    visited = set()
    expanded_count = 0
    
    while stack:
        path = stack.pop()
        node = path[-1]
        
        if node == goal:
            cost = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
            return path, round(cost, 2), expanded_count
            
        if node not in visited:
            visited.add(node)
            expanded_count += 1
            for neighbor in graph.get(node, {}):
                if neighbor not in visited:
                    stack.append(path + [neighbor])
    return None, 0, expanded_count

# 3. Uniform-Cost Search (UCS)
def ucs(graph, start, goal):
    pq = [(0, [start])]
    visited = {}
    expanded_count = 0
    
    while pq:
        cost, path = heapq.heappop(pq)
        node = path[-1]
        
        if node == goal:
            return path, round(cost, 2), expanded_count
            
        if node not in visited or cost < visited[node]:
            visited[node] = cost
            expanded_count += 1
            for neighbor, weight in graph.get(node, {}).items():
                if neighbor not in visited or cost + weight < visited.get(neighbor, float('inf')):
                    heapq.heappush(pq, (cost + weight, path + [neighbor]))
    return None, 0, expanded_count

# Helper function for IDS
def dls(graph, node, goal, depth, path, visited, expanded_count):
    if node == goal:
        return path, expanded_count
    if depth <= 0:
        return None, expanded_count
    visited.add(node)
    expanded_count[0] += 1
    for neighbor in graph.get(node, {}):
        if neighbor not in visited:
            res_path, count = dls(graph, neighbor, goal, depth - 1, path + [neighbor], visited.copy(), expanded_count)
            if res_path:
                return res_path, count
    return None, expanded_count[0]

# 4. Iterative Deepening Search (IDS)
def ids(graph, start, goal, max_depth=50):
    expanded_total = 0
    for depth in range(max_depth):
        expanded_count = [0]
        path, count = dls(graph, start, goal, depth, [start], set(), expanded_count)
        expanded_total += count
        if path:
            cost = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
            return path, round(cost, 2), expanded_total
    return None, 0, expanded_total