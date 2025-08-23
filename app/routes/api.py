"""
api.py
------
Flask REST API endpoints for ambulance routing system.
"""

from flask import Blueprint, jsonify, request
from app.backend.dataset_loader import dataset
from app.backend.astar import astar_search, astar_to_hospital
from app.backend.traffic_manager import traffic_manager

api_bp = Blueprint('api', __name__)

@api_bp.route('/get_map_data', methods=['GET'])
def get_map_data():
    nodes = dataset.get_nodes()
    edges = dataset.get_edges()
    return jsonify({"nodes": nodes, "edges": edges})


@api_bp.route('/find_route', methods=['POST'])
def find_route():
    data = request.get_json()
    if not data or 'start_node' not in data:
        return jsonify({"error": "Missing start_node"}), 400

    start_node = data['start_node']

    try:
        result = astar_search(start_node)
        if not result:
            return jsonify({"error": "No path found"}), 404
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/find_route_to_hospital', methods=['POST'])
def find_route_to_hospital():
    data = request.get_json()
    if not data or 'start_node' not in data or 'hospital_node' not in data:
        return jsonify({"error": "Missing start_node or hospital_node"}), 400

    start_node = data['start_node']
    hospital_node = data['hospital_node']

    try:
        result = astar_to_hospital(start_node, hospital_node)
        if not result:
            return jsonify({"error": "No path found"}), 404
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/block_road', methods=['POST'])
def block_road():
    """
    POST JSON: {"from": X, "to": Y}
    """
    data = request.get_json()
    if not data or 'from' not in data or 'to' not in data:
        return jsonify({"error": "Missing from/to IDs"}), 400

    from_id = data['from']
    to_id = data['to']

    success = traffic_manager.block_road(from_id, to_id)
    if success:
        return jsonify({"message": f"Road {from_id} ↔ {to_id} blocked successfully"})
    else:
        return jsonify({"error": "Failed to block road"}), 400

@api_bp.route('/unblock_road', methods=['POST'])
def unblock_road():
    """
    POST JSON: {"from": X, "to": Y}
    """
    data = request.get_json()
    if not data or 'from' not in data or 'to' not in data:
        return jsonify({"error": "Missing from/to IDs"}), 400

    from_id = data['from']
    to_id = data['to']

    success = traffic_manager.unblock_road(from_id, to_id)
    if success:
        return jsonify({"message": f"Road {from_id} ↔ {to_id} unblocked successfully"})
    else:
        return jsonify({"error": "Failed to unblock road"}), 400


@api_bp.route('/traffic_update', methods=['POST'])
def traffic_update():
    data = request.get_json()
    if not data or 'from' not in data or 'to' not in data or 'delay' not in data:
        return jsonify({"error": "Missing from/to/delay"}), 400

    from_id = data['from']
    to_id = data['to']
    delay = int(data['delay'])

    success = traffic_manager.update_traffic_delay(from_id, to_id, delay)
    if success:
        return jsonify({"message": f"Traffic delay updated for road {from_id} ↔ {to_id} to {delay} min"})
    else:
        return jsonify({"error": "Failed to update traffic delay"}), 400
    
@api_bp.route('/find_nearest_hospital', methods=['POST'])
def find_nearest_hospital():
    data = request.get_json()
    if not data or 'start_node' not in data:
        return jsonify({"error": "Missing start_node"}), 400

    start_node = data['start_node']

    try:
        from app.backend.astar import astar_to_nearest_hospital
        result = astar_to_nearest_hospital(start_node)

        if not result:
            return jsonify({"error": "No path found"}), 404

        path_coords = []
        for node_id in result["path"]:
            node = dataset.get_node_by_id(node_id)
            if node:
                path_coords.append({"lat": node["lat"], "lng": node["lon"]})

        nearest_hospital_id = result["path"][-1]
        nearest_hospital = dataset.get_node_by_id(nearest_hospital_id)
        hospital_name = nearest_hospital["name"] if nearest_hospital else "Unknown"

        return jsonify({
            "path": path_coords,
            "path_names": result["path_names"],
            "distance": round(result["total_distance_km"], 2),
            "eta": round(result["eta_minutes"], 1),
            "nearest_hospital": {"id": nearest_hospital_id, "name": hospital_name}
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
