# Route Finder — Dijkstra's Algorithm

A command-line Python program that finds both the shortest and fastest routes between two cities on a road map you enter. It uses Dijkstra's algorithm (with a min-heap) to compute optimal paths by distance and by travel time, then prints both results side by side so you can compare them.

## Features

- Accepts any road network typed in at the prompt
- Two-way roads with both distance (km) and speed limit (km/h) stored per edge
- Finds the shortest route (least total distance) and the fastest route (least total travel time)
- Reports total distance and travel time for both routes
- Detects when the two routes are identical
- Validates every input line and rejects bad data without crashing

## How It Works

**Graph representation.** The road network is stored as a dict of dicts. Each city maps to its neighbors, and each neighbor entry holds a `(distance, speed_limit)` tuple. Because roads are two-way, every edge is stored in both directions.

**Dijkstra with a min-heap.** The `dijkstra` function uses Python's `heapq` to maintain a priority queue of `(cost, city)` pairs. It pops the lowest-cost city, relaxes its neighbors, and pushes improved entries back onto the heap. Stale heap entries (where the popped cost exceeds the best known cost) are skipped. The algorithm stops early when the destination is popped.

**Why shortest ≠ fastest.** The shortest route minimizes total distance (`weight = distance`). The fastest route minimizes total travel time (`weight = distance / speed_limit`). A longer road with a high speed limit can be faster than a short road with a low speed limit, so the two routes can differ.

## Complexity

**Time:** O((V + E) log V), where V is the number of cities and E is the number of roads. Each vertex is extracted from the heap at most once, and each edge relaxation involves a heap push — both O(log V) operations.

**Space:** O(V + E) for the graph and the auxiliary data structures.

## How to Run

```
python route_finder.py
```

Requires Python 3.6 or later. No external packages needed.

## Example Session

```
Enter roads (city1 city2 distance_km speed_limit_kmph), blank line to finish:
A B 10 60
A C 4 30
C B 5 80
B D 10 120
C D 15 40

Start city: A
End city: D
Shortest route: A -> C -> D (19.0 km, 30.5 min)
Fastest route:  A -> B -> D (20.0 km, 15.0 min)
```

The shortest route (A → C → D) covers only 19 km but takes 30.5 minutes because of the 30 and 40 km/h speed limits. The fastest route (A → B → D) is 20 km but takes just 15 minutes because both roads have high speed limits (60 and 120 km/h).

## Limitations

- Does not support negative distances or speed limits (Dijkstra requires non-negative weights)
- No real-time traffic data — travel time is based only on the speed limit
- The road map is typed manually each time; there is no file import
- Does not handle one-way roads

## Possible Improvements

- Load road data from a CSV or JSON file
- Add a GUI or web interface with a map visualization
- Support one-way roads
- Add fuel cost or toll cost as a third optimization criterion
- Save and reload graphs between sessions
