# app/routes/ai.py
from flask import Blueprint, request, jsonify
import requests

ai_blueprint = Blueprint('ai', __name__)

@ai_blueprint.route('/code_analysis', methods=['POST'])
def analyze_code():
    code = request.json.get('code')
    sonar_url = 'http://your-sonarqube-url/api/analysis'
    response = requests.post(sonar_url, json={'code': code})
    analysis_result = response.json()
    return jsonify(analysis_result)