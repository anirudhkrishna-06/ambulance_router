
import math
from typing import Dict, List, Tuple, Optional
from app.backend.dataset_loader import dataset

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:    
    """
    Implementation of Haversisne
    """
    
    return


def heuristic(node_a: Dict, node_b: Dict) -> float:
    """
    For a couple of nodes, call the above function. Every node is a dict with parameters as keys. Refer other code file for it
    """
    return

def estimate_eta(distance_km: float, avg_speed_kmph: float = 30.0) -> float:
    return (distance_km / avg_speed_kmph) * 60.0

def get_node_by_id(node_id: int) -> Optional[Dict]:
    return dataset.get_node_by_id(node_id)


def get_node_coords(node_id: int) -> Tuple[float, float]:
    """
    To get the lat and long
    """
    return 


def get_node_name(node_id: int) -> str:
    """to get the node name"""
    return 


def find_nearest_node(lat: float, lon: float) -> Optional[Dict]:
    """
    To find the nearest node, Haversine a vechhu sort pannidu
    """


def get_hospitals() -> List[Dict]:
    return dataset.get_hospitals()


