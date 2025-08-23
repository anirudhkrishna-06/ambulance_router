import heapq
from typing import Dict, List, Tuple, Optional
from app.backend.graph_builder import GraphBuilder
from app.backend.utils import heuristic, estimate_eta, get_hospitals, get_node_by_id, get_node_name

PathResult = Dict[str, any]

def reconstruct_path(came_from: Dict[int, int], current: int) -> List[int]:
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(current)
    return path[::-1]

def astar_search(start_node_id: int, goal_node_id: int) -> Optional[PathResult]:
    graph_builder = GraphBuilder()
    graph = graph_builder.get_graph()

    open_set = []
    heapq.heappush(open_set, (0, start_node_id))
    came_from: Dict[int, int] = {}
    g_score = {node_id: float("inf") for node_id in graph}
    g_score[start_node_id] = 0
    f_score = {node_id: float("inf") for node_id in graph}

    start_node = get_node_by_id(start_node_id)
    goal_node = get_node_by_id(goal_node_id)
    f_score[start_node_id] = heuristic(start_node, goal_node)

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal_node_id:
            path = reconstruct_path(came_from, current)
            total_distance = sum(edge[2] for u, v in zip(path, path[1:]) 
                                 for edge in graph[u] if edge[0] == v)
            eta = estimate_eta(total_distance)
            return {
                "path": path,
                "path_names": [get_node_name(n) for n in path],
                "total_distance_km": total_distance,
                "eta_minutes": eta,
            }

        for neighbor, cost, distance, delay in graph.get(current, []):
            tentative_g = g_score[current] + cost
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(get_node_by_id(neighbor), goal_node)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

def astar_to_hospital(start_node_id: int, hospital_node_id: int) -> Optional[PathResult]:
    return astar_search(start_node_id, hospital_node_id)

def astar_to_nearest_hospital(start_node_id: int) -> Optional[PathResult]:
    hospitals = get_hospitals()  # List of hospital nodes
    shortest_result: Optional[PathResult] = None

    for hospital in hospitals:
        hospital_id = hospital["id"]
        result = astar_to_hospital(start_node_id, hospital_id)
        if result is None:
            continue
        if (shortest_result is None) or (result["total_distance_km"] < shortest_result["total_distance_km"]):
            shortest_result = result

    return shortest_result
