from flask import Flask, render_template, request, jsonify
import requests
from fetch_hospital import get_nearest_hospital

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_address', methods=['POST'])
def get_address():
    data = request.json
    lat = data.get('lat')
    lon = data.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Coordinates not provided'}), 400

    # Reverse geocode
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
    headers = {'User-Agent': 'FlaskApp'}
    response = requests.get(url, headers=headers)
    data = response.json()
    address = data.get('address', {})

    full_address = f"{address.get('road','')}, {address.get('suburb','')}, {address.get('city','')}, {address.get('state','')}, {address.get('postcode','')}, {address.get('country','')}"
    # full_address = "Shyambazar, North Kolkata, West Bengal, 700004, India"

    return jsonify({
        'latitude': lat,
        'longitude': lon,
        'full_address': full_address
    })

@app.route('/get_hospitals', methods=['POST'])
def get_hospitals():
    data = request.json
    user_address = data.get('address')

    if not user_address:
        return jsonify({'error': 'Address not provided'}), 400

    hospitals = get_nearest_hospital(user_address)
    return jsonify({'hospitals': hospitals})

if __name__ == '__main__':
    app.run(debug=True)
