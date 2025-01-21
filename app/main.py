from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO
from app.routes.ci_cd import ci_cd_blueprint
from app.routes.ai import ai_blueprint
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
from google.cloud import monitoring_v3
from google.oauth2 import service_account
import time
import os

# Initialize Flask app with static and template folders
app = Flask(__name__, static_folder='../frontend/public', template_folder='../frontend/public')

# Enable Cross-Origin Resource Sharing (CORS) for the app
# my frontend (which might be hosted on a different domain or port) needs to communicate with my Flask backend. Without CORS, the browser would block such cross-origin HTTP requests for security reasons.

CORS(app)

# Initialize SocketIO for real-time communication
socketio = SocketIO(app)

# Register blueprints for CI/CD and AI routes
app.register_blueprint(ci_cd_blueprint)
app.register_blueprint(ai_blueprint)

# Setup Google Cloud Monitoring
project_id = "fly-island"
client = monitoring_v3.MetricServiceClient()
project_name = f"projects/{project_id}"

def create_custom_metric(value):
    """
    Create a custom metric in Google Cloud Monitoring.

    Args:
        value (float): The value of the custom metric.
    """
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    )
    client = monitoring_v3.MetricServiceClient(credentials=credentials)
    project_id = credentials.project_id
    project_name = f"projects/{project_id}"
    
    series = monitoring_v3.types.TimeSeries()
    series.metric.type = 'custom.googleapis.com/my_metric'
    series.resource.type = 'global'
    series.resource.labels['project_id'] = 'fly-island'
    
    point = monitoring_v3.types.Point()
    point.value.double_value = value
    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)
    
    point.interval = monitoring_v3.types.TimeInterval()
    point.interval.end_time = Timestamp(seconds=seconds, nanos=nanos)
    
    series.points.append(point)
    
    client.create_time_series(name=project_name, time_series=[series])

def get_db_connection():
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URI'])
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def index():
    """
    Serve the main page of the application and log a custom metric.
    """
    create_custom_metric(1.0)  # Example metric value
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/ci_cd_status', methods=['GET'])
def get_ci_cd_status():
    """
    Endpoint to get the CI/CD status.
    
    Returns:
        Response: JSON response containing CI/CD status data.
    """
    data = [
        {"timestamp": "2024-12-10T22:47:00Z", "status": 1},
        {"timestamp": "2024-12-10T22:48:00Z", "status": 0},
    ]
    return jsonify(data)

@app.route('/update_pipeline_status', methods=['POST'])
def update_pipeline_status():
    """
    Endpoint to update the pipeline status and emit a SocketIO event.
    
    Returns:
        Response: JSON response indicating the status of the update.
    """
    data = [
        {"timestamp": "2024-12-10T22:47:00Z", "status": 1},
        {"timestamp": "2024-12-10T22:48:00Z", "status": 0},
    ]
    socketio.emit('pipeline_status_update', data)
    return jsonify({'status': 'success'})

@app.route('/db_test')
def db_test():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500
    try:
        cur = conn.cursor()
        cur.execute("SELECT version()")
        db_version = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({'db_version': db_version})
    except Exception as e:
        print(f"Database query error: {e}")
        return jsonify({'error': 'Database query failed'}), 500


@socketio.on('connect')
def handle_connect():
    """
    Handle a new client connection and log a custom metric.
    """
    create_custom_metric(1.0)  # Example metric value
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    """
    Handle a client disconnection and log a custom metric.
    """
    create_custom_metric(0.0)  # Example metric value
    print('Client disconnected')

@socketio.on('request_pipeline_status')
def handle_request_pipeline_status():
    """
    Handle a request for pipeline status and emit the current status.
    """
    data = [
        {"timestamp": "2024-12-10T22:47:00Z", "status": 1},
        {"timestamp": "2024-12-10T22:48:00Z", "status": 0},
    ]
    emit('pipeline_status_update', data)

if __name__ == '__main__':
    # Run the Flask app with SocketIO on the specified host and port
    socketio.run(app, host='0.0.0.0', port=8080)
