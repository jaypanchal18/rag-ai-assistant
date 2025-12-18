from flask import Flask
import pinecone
import tensorflow as tf
import os

def create_app():
    app = Flask(__name__)

    # Load configuration from environment variables or a config file
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
    app.config['PINECONE_API_KEY'] = os.getenv('PINECONE_API_KEY')
    app.config['PINECONE_ENV'] = os.getenv('PINECONE_ENV', 'us-west1-gcp')

    # Initialize Pinecone
    try:
        pinecone.init(api_key=app.config['PINECONE_API_KEY'], environment=app.config['PINECONE_ENV'])
    except Exception as e:
        app.logger.error(f'Failed to initialize Pinecone: {e}')
        raise

    # Initialize TensorFlow (if needed)
    try:
        tf.config.experimental.set_memory_growth(tf.config.list_physical_devices('GPU')[0], True)
    except Exception as e:
        app.logger.warning(f'TensorFlow initialization warning: {e}')

    # Register blueprints or routes here
    from .routes import main
    app.register_blueprint(main)

    return app

app = create_app()