import tensorflow as tf
from flask import Flask, request, jsonify
import pinecone
import numpy as np

app = Flask(__name__)

# Initialize Pinecone
pinecone.init(api_key='YOUR_PINECONE_API_KEY', environment='YOUR_PINECONE_ENV')

# Create a Pinecone index
index_name = 'nlp-index'
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=768)

index = pinecone.Index(index_name)

# Load pre-trained TensorFlow model for NLP
model = tf.keras.models.load_model('path/to/your/nlp_model')

def preprocess_text(text):
    # Implement text preprocessing steps
    text = text.lower()
    # Add more preprocessing as needed
    return text

def get_embeddings(text):
    # Convert text to embeddings using the model
    processed_text = preprocess_text(text)
    embeddings = model.predict(np.array([processed_text]))
    return embeddings

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.json
        user_query = data.get('query', '')
        
        if not user_query:
            return jsonify({'error': 'No query provided'}), 400
        
        embeddings = get_embeddings(user_query)
        
        # Query Pinecone for similar items
        results = index.query(embeddings.tolist(), top_k=5)
        
        return jsonify(results), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)