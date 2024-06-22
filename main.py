import os
from flask import Flask, request, jsonify, render_template
import requests
import time

app = Flask(__name__)

# Load the Gemini API key from the environment variable
GEMINI_API_TOKEN = os.getenv('GEMINI_API_TOKEN')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    description = request.json.get('description')
    if not description:
        return jsonify({'error': 'No description provided'}), 400

    try:
        # Send the request to Gemini's API
        response = requests.post(
            'https://api.gemini.com/v1/images/generate',
            headers={
                'Authorization': f'Bearer {GEMINI_API_TOKEN}',
                'Content-Type': 'application/json'
            },
            json={
                'prompt': description
            }
        )

        # Check for errors in the API request
        if response.status_code != 201:
            return jsonify({'error': response.json().get('detail', 'Unknown error')}), 500

        # Get the generated image URL from the response
        image_url = response.json().get('image_url')
        if not image_url:
            return jsonify({'error': 'Image generation failed'}), 500

        return jsonify({'image_url': image_url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
