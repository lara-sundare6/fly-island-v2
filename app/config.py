import os

DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://<USERNAME>:<PASSWORD>@<INSTANCE_CONNECTION_NAME>/<DATABASE_NAME>')