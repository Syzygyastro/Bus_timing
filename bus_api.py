from flask import Flask, jsonify
import requests
import os  # Import os module to access environment variables
from mangum import Mangum

app = Flask(__name__)

@app.route('/bus-timings', methods=['GET'])
def bus_timings():
    # Retrieve API key from environment variable
    app_key = os.getenv('TFL_API_KEY')  # Provide a default or ensure it's set in the environment

    bus_stop_ids = [('Harrow View West', '490008888S'), ('Harrow View', '490013383E')]
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

handler = Mangum(app)  # This makes the Flask app compatible with AWS Lambda and Vercel's serverless platform
