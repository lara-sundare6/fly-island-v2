# fly-island

## Deployment Instructions

### Google Cloud

1. Install the Google Cloud SDK:
    ```sh
    curl https://sdk.cloud.google.com | bash
    exec -l $SHELL
    gcloud init
    ```

2. Deploy the app:
    ```sh
    gcloud app deploy
    ```

### Docker

1. Install Docker from [Docker's official website](https://docs.docker.com/get-docker/).

2. Build the Docker image:
    ```sh
    docker build -t gcr.io/your-project-id/your-app .
    ```

3. Push the Docker container:
    ```sh
    docker push gcr.io/your-project-id/your-app
    ```

4. Deploy to Google Cloud Run
    ```
    gcloud run deploy your-app \
        --image gcr.io/your-project-id/your-app \
        --platform managed \
        --region your-region \
        --allow-unauthenticated
    ```
    
### Virtual Environment

1. Activate the virtual environment:
    - On Unix or MacOS:
        ```sh
        source venv/bin/activate
        ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

### Flask

1. Set the Flask app environment variable:
    ```sh
    export FLASK_APP=app.py
    ```

2. Run the Flask application:
    ```sh
    flask run
    ```

Feel free to customize these instructions as per your project's requirements. You can update the README.md file directly in the repository with these instructions.
