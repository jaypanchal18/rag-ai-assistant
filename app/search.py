from flask import Blueprint, request, jsonify
import pinecone
import tensorflow as tf
import numpy as np

search_bp = Blueprint('search', __name__)

# Initialize Pinecone
pinecone.init(api_key='YOUR_PINECONE_API_KEY', environment='YOUR_PINECONE_ENVIRONMENT')
index = pinecone.Index('YOUR_INDEX_NAME')

# Load your NLP model (e.g., a pre-trained TensorFlow model)
model = tf.keras.models.load_model('path/to/your/nlp_model')

@search_bp.route('/search', methods=['POST'])
def search():
    try:
        data = request.json
        query = data.get('query', '')

        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400

        # Preprocess the query using the NLP model
        query_vector = model.predict(np.array([query]))  # Adjust based on your model's input requirements
        query_vector = query_vector[0].tolist()  # Convert to list for Pinecone

        # Perform the search in Pinecone
        results = index.query(queries=[query_vector], top_k=10)

        # Format the results
        documents = [{'id': match['id'], 'score': match['score']} for match in results['matches']]

        return jsonify({'results': documents}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Register the blueprint in your main app file
# app.register_blueprint(search_bp)