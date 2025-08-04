from flask import Blueprint, jsonify
import json
import os

device_bp = Blueprint('device', __name__)

@device_bp.route('/device_info')
def get_device_info():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'device_info.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        device_info = json.load(f)
    return jsonify(device_info)
