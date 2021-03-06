import os
from pathlib import Path

from dotenv import load_dotenv

dotenv_path = str(Path(Path(__file__).parent.name + '/../.env').resolve())
default_local_storage_path = str(
    Path(Path(__file__).parent.name + 'app/static/uploads').resolve())
load_dotenv(dotenv_path)


class Config:
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    NAME = os.getenv('NAME', 'Flask Sample')
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    DEBUG = False
    APP_HOST = os.getenv('APP_HOST', '127.0.0.1')
    APP_PORT = os.getenv('APP_PORT', '5000')
    APP_URL = os.getenv('APP_URL', 'http://localhost')

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'.format(
        **{
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'name': os.getenv('DB_NAME', 'default_name'),
        })

    if FLASK_ENV != 'test':
        SQLALCHEMY_POOL_SIZE = int(os.getenv('SQLALCHEMY_POOL_SIZE', 10))
        SQLALCHEMY_MAX_OVERFLOW = int(os.getenv('SQLALCHEMY_MAX_OVERFLOW', 20))
    if FLASK_ENV == 'test':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        # SQLALCHEMY_ECHO = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STORAGE_TYPE = os.getenv('STORAGE_TYPE', 'local')
    POLL_ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

    AWS_KEY = os.getenv('AWS_KEY', '')
    AWS_SECRET = os.getenv('AWS_SECRET', '')
    STORAGE_S3_REGION = os.getenv('STORAGE_S3_REGION', '')
    STORAGE_S3_BUCKET_NAME = os.getenv('STORAGE_S3_BUCKET_NAME', '')

    MINIO_HOST = os.getenv('MINIO_HOST', '')
    MINIO_PORT = os.getenv('MINIO_PORT', '')
    MINIO_KEY = os.getenv('MINIO_KEY', '')
    MINIO_SECRET = os.getenv('MINIO_SECRET', '')
    STORAGE_MINIO_BUCKET_NAME = os.getenv('STORAGE_MINIO_BUCKET_NAME', '')

    STORAGE_LOCAL_DIRECTORY = os.getenv('STORAGE_LOCAL_DIRECTORY',
                                        default_local_storage_path)

    SLACK_ENABLED = bool(os.getenv('SLACK_ENABLED', False))
    SLACK_WEBHOOK_USER = os.getenv('SLACK_WEBHOOK_USER', 'flask-bot')
    SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', '')
    SLACK_CHANNEL_NAME = os.getenv('SLACK_CHANNEL_NAME', '')

    SESSION_TYPE = os.getenv('SESSION_TYPE')
    SESSION_FILE_DIR = os.getenv('SESSION_FILE_DIR')
    SESSION_FILE_THRESHOLD = int(os.getenv('SESSION_FILE_THRESHOLD'))
    TOKEN_EXPIRED_IN_DAYS = int(os.getenv('TOKEN_EXPIRED_IN_DAYS', 1))

    SLACK_ENABLED = bool(os.getenv('SLACK_ENABLED', False))
    SLACK_WEBHOOK_USER = os.getenv('SLACK_WEBHOOK_USER', 'flask-bot')
    SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', '')
    SLACK_CHANNEL_NAME = os.getenv('SLACK_CHANNEL_NAME', '')

    CACHE_TYPE = os.getenv('CACHE_TYPE', 'filesystem')
    CACHE_DIR = os.getenv('CACHE_DIR', 'local_caches')
    CACHE_TIMEOUT_SECONDS = int(os.getenv('CACHE_TIMEOUT_SECONDS', 120))
