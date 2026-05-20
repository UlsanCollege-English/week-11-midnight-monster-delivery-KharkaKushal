from math import inf
import heapq

HAUNTED_CITY = {
    "Crypt Kitchen": {
        "Fog Alley": 2,
        "Bone Bridge": 5,
    },
    "Fog Alley": {
        "Moon Bridge": 1,
        "Goblin Market": 4,
    },
    "Bone Bridge": {
        "Goblin Market": 1,
    },
    "Moon Bridge": {
        "Werewolf Den": 5,
    },
    "Goblin Market": {
        "Werewolf Den": 2,
    },
    "Werewolf Den": {
        "Vampire Tower": 2,
    },
    "Vampire Tower": {},
}


def validate_haunted_map(graph):
    """Validate the haunted graph."""

    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():

            if weight <= 0:
                raise ValueError("Weights must be positive")

            if neighbor not in graph:
                raise ValueError("Neighbor node missing")


def monster_delivery_costs(graph, start):
    """Return shortest costs from start node."""

    validate_haunted_map(graph)

    if start not in graph:
        raise ValueError("Missing start node")

    distances = {node: inf for node in graph}
    distances[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:
        current_cost, current_node = heapq.heappop(priority_queue)

        if current_cost > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            new_cost = current_cost + weight

            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                heapq.heappush(
                    priority_queue,
                    (new_cost, neighbor),
                )

    return distances


def shortest_monster_delivery(graph, start, target):
    """Return shortest path and cost."""

    try:
        validate_haunted_map(graph)
    except ValueError:
        return inf, []

    if start not in graph or target not in graph:
        return inf, []

    if start == target:
        return 0, [start]

    distances = {node: inf for node in graph}
    previous = {}

    distances[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:
        current_cost, current_node = heapq.heappop(priority_queue)

        if current_cost > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            new_cost = current_cost + weight

            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                previous[neighbor] = current_node

                heapq.heappush(
                    priority_queue,
                    (new_cost, neighbor),
                )

    if distances[target] == inf:
        return inf, []

    path = []
    current = target

    while current != start:
        path.append(current)
        current = previous[current]

    path.append(start)
    path.reverse()

    return distances[target], path