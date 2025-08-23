from typing import Dict, List, Tuple
from app.backend.dataset_loader import dataset

Neighbor = Tuple[int, float, float, int]

class GraphBuilder:
    def __init__(self):
        self.graph: Dict[int, List[Neighbor]] = {}
        self.build_graph()

 
    def build_graph(self) -> None:
        self.graph = {}

        for edge in dataset.get_edges():
            if edge.get("blocked"):
                continue 
            from_id = edge["from"]
            to_id = edge["to"]
            distance = float(edge["distance"])
            delay = int(edge.get("traffic_delay", 0))
            cost = distance + delay * 0.1 
            self.graph.setdefault(from_id, []).append((to_id, cost, distance, delay))
            self.graph.setdefault(to_id, []).append((from_id, cost, distance, delay))

    def get_neighbors(self, node_id: int) -> List[Neighbor]:
        return self.graph.get(node_id, [])

    def get_graph(self) -> Dict[int, List[Neighbor]]:
        return self.graph

    def get_node_ids(self) -> List[int]:
        return list(self.graph.keys())

    def refresh(self) -> None:
        self.build_graph()

