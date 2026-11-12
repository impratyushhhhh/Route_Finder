import heapq

def build_graph(roads):
    graph = {}
    for city_a, city_b, dist, speed in roads:
        graph.setdefault(city_a, {})[city_b] = (dist, speed)
        graph.setdefault(city_b, {})[city_a] = (dist, speed)
    return graph

def dijkstra(graph, start, end, weight_fn):
    best, prev, heap = {start: 0}, {start: None}, [(0, start)]
    while heap:
        cost, city = heapq.heappop(heap)
        if city == end: break
        if cost > best.get(city, float("inf")): continue
        for nb, (d, s) in graph.get(city, {}).items():
            w = cost + weight_fn(d, s)
            if w < best.get(nb, float("inf")):
                best[nb], prev[nb] = w, city
                heapq.heappush(heap, (w, nb))
    return best, prev

def rebuild_path(prev, end):
    path, cur = [], end
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur)
    path.reverse()
    return path

def compute_totals(graph, path):
    edges = [graph[path[i]][path[i + 1]] for i in range(len(path) - 1)]
    return sum(d for d, _ in edges), sum(d / s * 60 for d, s in edges)

def read_roads():
    roads = []
    print("Enter roads (city1 city2 distance_km speed_limit_kmph), blank line to finish:")
    while True:
        line = input().strip()
        if not line: return roads
        parts = line.split()
        if len(parts) != 4:
            print("Error: each line must have exactly 4 parts."); continue
        try: dist, speed = float(parts[2]), float(parts[3])
        except ValueError:
            print("Error: distance and speed limit must be numbers."); continue
        if dist <= 0 or speed <= 0:
            print("Error: distance and speed limit must be positive."); continue
        roads.append((parts[0], parts[1], dist, speed))

def ask_city(prompt, graph):
    while True:
        city = input(prompt).strip()
        if city in graph: return city
        print(f"City '{city}' not found in the graph. Try again.")

if __name__ == "__main__":
    graph = build_graph(read_roads())
    start, end = ask_city("Start city: ", graph), ask_city("End city: ", graph)
    sb, sp = dijkstra(graph, start, end, lambda d, s: d)
    fb, fp = dijkstra(graph, start, end, lambda d, s: d / s)
    if end not in sb:
        print("No route found.")
    else:
        s_path, f_path = rebuild_path(sp, end), rebuild_path(fp, end)
        sd, st = compute_totals(graph, s_path)
        fd, ft = compute_totals(graph, f_path)
        print(f"Shortest route: {' -> '.join(s_path)} ({sd:.1f} km, {st:.1f} min)")
        print(f"Fastest route:  {' -> '.join(f_path)} ({fd:.1f} km, {ft:.1f} min)")
        if s_path == f_path:
            print("The shortest and fastest routes are the same.")
