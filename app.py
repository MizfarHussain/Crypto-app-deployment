import os
from flask import Flask, jsonify
import requests

# Initialize the Flask application
app = Flask(__name__)

# CoinGecko API URL for fetching cryptocurrency prices
# We are fetching prices for Bitcoin, Ethereum, and Ripple in USD.
API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,ripple&vs_currencies=usd"

@app.route('/')
def get_crypto_prices():
    """
    API endpoint to fetch and return cryptocurrency prices.
    This function makes a GET request to the CoinGecko API.
    """
    try:
        # Make the request to the external API
        response = requests.get(API_URL)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        # Handle potential network errors or API failures
        return jsonify({"error": f"Could not fetch data from CoinGecko API: {e}"}), 503

@app.route('/health')
def health_check():
    """
    Health check endpoint for the load balancer or container orchestrator (ECS).
    Returns a simple JSON response to indicate the service is running.
    """
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    # This block is for running the app directly with 'python app.py' for local development.
    # It runs on port 5000 by default.
    app.run(host='0.0.0.0', port=5000, debug=True)
