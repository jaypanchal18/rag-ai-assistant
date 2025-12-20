import os
import pinecone
from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np

app = Flask(__name__)

# Initialize Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
INDEX_NAME = "document-search"

try:
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
    if INDEX_NAME not in pinecone.list_indexes():
        pinecone.create_index(INDEX_NAME, dimension=768)  # Assuming 768-dimensional embeddings
    index = pinecone.Index(INDEX_NAME)
except Exception as e:
    print(f"Error initializing Pinecone: {e}")

def embed_text(text):
    model = tf.keras.models.load_model('path/to/your/model')  # Load your TensorFlow model
    embeddings = model.predict(np.array([text]))  # Assuming the model takes a single text input
    return embeddings[0]

@app.route('/add_document', methods=['POST'])
def add_document():
    try:
        data = request.json
        document_id = data['id']
        document_text = data['text']
        embedding = embed_text(document_text)
        index.upsert([(document_id, embedding)])
        return jsonify({"message": "Document added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/search', methods=['POST'])
def search():
    try:
        query = request.json['query']
        query_embedding = embed_text(query)
        results = index.query(query_embedding, top_k=5)  # Retrieve top 5 similar documents
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)