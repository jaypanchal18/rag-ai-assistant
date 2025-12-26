import os
import sys
import logging
from flask import Flask
import pinecone
import tensorflow as tf

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
def load_env_variables():
    try:
        os.environ['FLASK_ENV'] = os.getenv('FLASK_ENV', 'production')
        os.environ['PINECONE_API_KEY'] = os.getenv('PINECONE_API_KEY')
        os.environ['TENSORFLOW_MODEL_PATH'] = os.getenv('TENSORFLOW_MODEL_PATH')
        if not os.environ['PINECONE_API_KEY']:
            raise ValueError("PINECONE_API_KEY is not set.")
        if not os.environ['TENSORFLOW_MODEL_PATH']:
            raise ValueError("TENSORFLOW_MODEL_PATH is not set.")
    except Exception as e:
        logging.error(f"Error loading environment variables: {e}")
        sys.exit(1)

# Initialize Pinecone
def init_pinecone():
    try:
        pinecone.init(api_key=os.environ['PINECONE_API_KEY'], environment='us-west1-gcp')
        logging.info("Pinecone initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize Pinecone: {e}")
        sys.exit(1)

# Load TensorFlow model
def load_tensorflow_model():
    try:
        model = tf.keras.models.load_model(os.environ['TENSORFLOW_MODEL_PATH'])
        logging.info("TensorFlow model loaded successfully.")
        return model
    except Exception as e:
        logging.error(f"Failed to load TensorFlow model: {e}")
        sys.exit(1)

# Main deployment preparation function
def prepare_deployment():
    load_env_variables()
    init_pinecone()
    model = load_tensorflow_model()
    return model

if __name__ == "__main__":
    model = prepare_deployment()
    app.run(host='0.0.0.0', port=5000)