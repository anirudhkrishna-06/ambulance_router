import json
import os
from typing import Dict, List, Any, Optional

DATA_FILE = os.path.join(os.path.dirname(__file__), "../../data/roads.json")

class DatasetLoader:
    def __init__(self, filepath: str = DATA_FILE):
        self.filepath = filepath
        self.data = self._load_dataset()
    def _load_dataset(self) -> Dict[str, Any]:
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Dataset not found: {self.filepath}")

        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_dataset(self) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def get_nodes(self) -> List[Dict[str, Any]]:
        return self.data.get("nodes", [])

    def get_node_by_id(self, node_id: int) -> Optional[Dict[str, Any]]:
        return next((n for n in self.get_nodes() if n["id"] == node_id), None)

    def get_hospitals(self) -> List[Dict[str, Any]]:
        return [n for n in self.get_nodes() if n["type"] == "hospital"]

    def get_edges(self) -> List[Dict[str, Any]]:
        return self.data.get("edges", [])

    def get_edges_from(self, node_id: int) -> List[Dict[str, Any]]:
        return [e for e in self.get_edges() if e["from"] == node_id]

    
    def block_edge(self, from_id: int, to_id: int) -> bool:
        updated = False
        for edge in self.get_edges():
            if (edge["from"] == from_id and edge["to"] == to_id) or \
               (edge["from"] == to_id and edge["to"] == from_id):
                edge["blocked"] = True
                updated = True
        if updated:
            self.save_dataset()
        return updated

    def unblock_edge(self, from_id: int, to_id: int) -> bool:
        updated = False
        for edge in self.get_edges():
            if (edge["from"] == from_id and edge["to"] == to_id) or \
               (edge["from"] == to_id and edge["to"] == from_id):
                edge["blocked"] = False
                updated = True
        if updated:
            self.save_dataset()
        return updated

    def update_traffic_delay(self, from_id: int, to_id: int, delay: int) -> bool:
        updated = False
        for edge in self.get_edges():
            if (edge["from"] == from_id and edge["to"] == to_id) or \
               (edge["from"] == to_id and edge["to"] == from_id):
                edge["traffic_delay"] = delay
                updated = True
        if updated:
            self.save_dataset()
        return updated


    
