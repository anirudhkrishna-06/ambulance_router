
import math
from typing import Dict, List, Tuple, Optional
from app.backend.dataset_loader import dataset

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:    
    """
    Implementation of Haversisne
    """
    R = 6371.0  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c
    


def heuristic(node_a: Dict, node_b: Dict) -> float:
    """
    For a couple of nodes, call the above function. Every node is a dict with parameters as keys. Refer other code file for it
    """
    return haversine_distance(node_a["lat"], node_a["lon"], node_b["lat"], node_b["lon"])

def estimate_eta(distance_km: float, avg_speed_kmph: float = 30.0) -> float:
   return (distance_km / avg_speed_kmph) * 60.0

def get_node_by_id(node_id: int) -> Optional[Dict]:
    return dataset.get_node_by_id(node_id)


def get_node_coords(node_id: int) -> Tuple[float, float]:
    node = dataset.get_node_by_id(node_id)
    return (node["lat"], node["lon"]) if node else (0.0, 0.0)


def get_node_name(node_id: int) -> str:
    node = dataset.get_node_by_id(node_id)
    return node["name"] if node else "Unknown"


def find_nearest_node(lat: float, lon: float) -> Optional[Dict]:
    all_nodes = dataset.get_nodes()
    if not all_nodes:
        return None
    nearest = min(all_nodes, key=lambda n: haversine_distance(lat, lon, n["lat"], n["lon"]))
    return nearest


def get_hospitals() -> List[Dict]:
    return dataset.get_hospitals()


