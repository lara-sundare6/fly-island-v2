# Fly Island

Fly Island is a web application that integrates with Google Cloud Monitoring to create custom metrics and provides CI/CD status updates. The application is built using Flask, Flask-SocketIO, and React.

## Features

- Create custom metrics in Google Cloud Monitoring
- Serve a React frontend
- Provide CI/CD status updates via a REST API
- Real-time updates using SocketIO

## Prerequisites

- Python 3.8+
- Node.js and npm
- Google Cloud account with Monitoring API enabled
- Google Cloud credentials file

## Usage

- Access the application at `http://localhost:5000`
- The root route (`/`) serves the React frontend
- The `/ci_cd_status` route provides CI/CD status updates
- Real-time updates are handled via SocketIO

## Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/fly-island.git
    cd fly-island
    ```

2. Set up the Python environment:

    ```sh
    python3 -m venv myenv
    source myenv/bin/activate
    pip install -r requirements.txt
    ```

3. Set up the React frontend:

    ```sh
    cd frontend
    npm install
    npm run build
    cd ..
    ```

4. Set the Google Cloud credentials:

    ```sh
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
    ```

5. Run the Flask application:

    ```sh
    flask run

Feel free to customize these instructions as per your project's requirements. You can update the README.md file directly in the repository with these instructions.
