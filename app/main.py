from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
from app.routes.ci_cd import ci_cd_blueprint
from app.routes.ai import ai_blueprint
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import time

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# Register blueprints
app.register_blueprint(ci_cd_blueprint)
app.register_blueprint(ai_blueprint)

# Google Cloud Monitoring setup
project_id = "fly-island"
client = monitoring_v3.MetricServiceClient()
project_name = f"projects/{project_id}"

# app/main.py
def create_custom_metric(value):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/my_metric"
    series.resource.type = "global"

    point = series.points.add()
    point.value.double_value = value
    now = Timestamp()
    now.GetCurrentTime()
    point.interval.end_time.seconds = int(now.seconds)
    point.interval.end_time.nanos = int(now.nanos)

    client.create_time_series(name=project_name, time_series=[series])


@app.route('/')
def index():
    create_custom_metric(1.0)  # Example metric value
    return app.send_static_file('index.html')

@app.route('/ci_cd_status', methods=['GET'])
def get_ci_cd_status():
    # Fetch and return CI/CD status data
    data = [
        {"timestamp": "2024-12-10T22:47:00Z", "status": 1},
        {"timestamp": "2024-12-10T22:48:00Z", "status": 0},
        # Add more data points as needed
    ]
    return jsonify(data)

@app.route('/update_pipeline_status', methods=['POST'])
def update_pipeline_status():
    # Fetch the latest pipeline status and emit it to all connected clients
    data = [
        {"timestamp": "2024-12-10T22:47:00Z", "status": 1},
        {"timestamp": "2024-12-10T22:48:00Z", "status": 0},
        # Add more data points as needed
    ]
    socketio.emit('pipeline_status_update', data)
    return jsonify({'status': 'success'})

@socketio.on('connect')
def handle_connect():
    create_custom_metric(1.0)  # Example metric value
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    create_custom_metric(0.0)  # Example metric value
    print('Client disconnected')

@socketio.on('request_pipeline_status')
def handle_request_pipeline_status():
    # Emit the current pipeline status to the client
    data = [
        {"timestamp": "2024-12-10T22:47:00Z", "status": 1},
        {"timestamp": "2024-12-10T22:48:00Z", "status": 0},
        # Add more data points as needed
    ]
    emit('pipeline_status_update', data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)