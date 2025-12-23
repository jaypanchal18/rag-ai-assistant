from flask import Blueprint, jsonify, request
import requests
import os

api_integration = Blueprint('api_integration', __name__)

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

@api_integration.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    try:
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}')
        response.raise_for_status()
        weather_data = response.json()
        return jsonify(weather_data), 200
    except requests.exceptions.HTTPError as http_err:
        return jsonify({'error': str(http_err)}), 500
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@api_integration.route('/news', methods=['GET'])
def get_news():
    category = request.args.get('category', 'general')
    try:
        response = requests.get(f'https://newsapi.org/v2/top-headlines?category={category}&apiKey={NEWS_API_KEY}')
        response.raise_for_status()
        news_data = response.json()
        return jsonify(news_data), 200
    except requests.exceptions.HTTPError as http_err:
        return jsonify({'error': str(http_err)}), 500
    except Exception as err:
        return jsonify({'error': str(err)}), 500