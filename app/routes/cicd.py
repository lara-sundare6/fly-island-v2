from flask import Blueprint, jsonify

ci_cd_blueprint = Blueprint('ci_cd', __name__)

@ci_cd_blueprint.route('/ci_cd_data', methods=['GET'])
def get_ci_cd_data():
    # Fetch and process CI/CD data from Jenkins, GitLab CI, etc.
    data = {
        "pipeline": "example_pipeline",
        "status": "success",
        "stages": [
            {"name": "build", "status": "success"},
            {"name": "test", "status": "success"},
            {"name": "deploy", "status": "success"}
        ]
    }
    return jsonify(data)
