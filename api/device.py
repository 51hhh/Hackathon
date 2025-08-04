from flask import Blueprint, jsonify
import json

device_bp = Blueprint('device', __name__)

@device_bp.route('/device_info')
def get_device_info():
    with open('./data/device_info.json', 'r', encoding='utf-8') as f:
        device_info = json.load(f)
    return jsonify(device_info)
