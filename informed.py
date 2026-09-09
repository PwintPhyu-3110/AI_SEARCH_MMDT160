import heapq
import math

# မြို့ နှစ်ခုကြား တိုက်ရိုက်အကွာအဝေး (Straight-line Distance) ကို တွက်ပေးသော Heuristic Formula
def haversine(coord1, coord2):
    R = 6371.0 # ကမ္ဘာမြေ၏ အချင်းဝက် (km)
    lat1, lon1 = math.radians(coord1['lat']), math.radians(coord1['lon'])
    lat2, lon2 = math.radians(coord2['lat']), math.radians(coord2['lon'])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

# 5. Greedy Best-First Search
def greedy_bfs(graph, nodes, start, goal):
    goal_coord = nodes[goal]
    pq = [(haversine(nodes[start], goal_coord), [start])]
    visited = set()
    expanded_count = 0
    
    while pq:
        h, path = heapq.heappop(pq)
        node = path[-1]
        
        if node == goal:
            cost = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
            return path, round(cost, 2), expanded_count
            
        if node not in visited:
            visited.add(node)
            expanded_count += 1
            for neighbor in graph.get(node, {}):
                if neighbor not in visited:
                    heapq.heappush(pq, (haversine(nodes[neighbor], goal_coord), path + [neighbor]))
    return None, 0, expanded_count

# 6. A* Search
def a_star(graph, nodes, start, goal):
    goal_coord = nodes[goal]
    pq = [(haversine(nodes[start], goal_coord), 0, [start])]
    visited = {}
    expanded_count = 0
    
    while pq:
        f, g, path = heapq.heappop(pq)
        node = path[-1]
        
        if node == goal:
            return path, round(g, 2), expanded_count
            
        if node not in visited or g < visited[node]:
            visited[node] = g
            expanded_count += 1
            for neighbor, weight in graph.get(node, {}).items():
                new_g = g + weight
                if neighbor not in visited or new_g < visited.get(neighbor, float('inf')):
                    h_val = haversine(nodes[neighbor], goal_coord)
                    heapq.heappush(pq, (new_g + h_val, new_g, path + [neighbor]))
    return None, 0, expanded_count