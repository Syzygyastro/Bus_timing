from flask import Flask, jsonify, request
import requests
import datetime
from mangum import Mangum

app = Flask(__name__)

@app.route('/bus-timings', methods=['GET'])
def bus_timings():
    bus_stop_ids = [('Harrow View West', '490008888S'), ('Harrow View', '490013383E')]
    app_key = 'a7ab5d5787f942c699ffa77f18cc0b82'  # Ensure your API key is kept secure
    results = []
    for name, stop_id in bus_stop_ids:
        url = f"https://api.tfl.gov.uk/StopPoint/{stop_id}/Arrivals?app_key={app_key}"
        response = requests.get(url)
        if response.status_code == 200:
            buses = sorted(response.json(), key=lambda x: x['timeToStation'])
            bus_info = [f"Bus {bus['lineName']} to {bus['destinationName']} arrives in {int(bus['timeToStation']/60)} mins" for bus in buses]
            results.append({name: bus_info})
        else:
            results.append({name: "Failed to retrieve data"})
    return jsonify(results)

handler = Mangum(app)
