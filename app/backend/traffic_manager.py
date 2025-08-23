from app.backend.dataset_loader import dataset
from app.backend.graph_builder import GraphBuilder
from typing import List, Dict


class TrafficManager:
    def __init__(self):
        self.graph_builder = GraphBuilder()

    def block_road(self, from_id: int, to_id: int) -> bool:
        updated = dataset.block_edge(from_id, to_id)
        if updated:
            self.graph_builder.refresh()
        return updated

    def unblock_road(self, from_id: int, to_id: int) -> bool:
        updated = dataset.unblock_edge(from_id, to_id)
        if updated:
            self.graph_builder.refresh()
        return updated

    def update_traffic_delay(self, from_id: int, to_id: int, delay: int) -> bool:
        updated = dataset.update_traffic_delay(from_id, to_id, delay)
        if updated:
            self.graph_builder.refresh()
        return updated

    def simulate_traffic(self, updates: List[Dict]) -> None:
        for upd in updates:
            from_id = upd.get("from")
            to_id = upd.get("to")
            delay = upd.get("delay", 0)
            blocked = upd.get("blocked", False)

            if blocked:
                self.block_road(from_id, to_id)
            else:
                self.unblock_road(from_id, to_id)

            self.update_traffic_delay(from_id, to_id, delay)


traffic_manager = TrafficManager()