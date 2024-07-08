import json
from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
api_key = config['TFL_API_KEY']

def fetch_bus_timings():
    bus_stop_ids = {
        'Harrow View West': '490008888S',
        'Harrow View': '490013383E'
    }
    results = {}
    for name, stop_id in bus_stop_ids.items():
        url = f"https://api.tfl.gov.uk/StopPoint/{stop_id}/Arrivals?app_key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            buses = sorted(response.json(), key=lambda x: x['timeToStation'])
            bus_info = [f"Bus {bus['lineName']} to {bus['destinationName']} arrives in {int(bus['timeToStation']/60)} mins" for bus in buses]
            results[name] = bus_info
        else:
            results[name] = "Failed to retrieve data"
    return jsonify(results)

@app.route('/', methods=['GET'])
def home():
    results = fetch_bus_timings()
    return jsonify(results)