from flask import Flask, request, jsonify
import pinecone
import os

app = Flask(__name__)

# Initialize Pinecone
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV"))

# Create or connect to an index
index_name = "document-index"
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name)
index = pinecone.Index(index_name)

@app.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        try:
            # Read the file content
            content = file.read().decode('utf-8')
            # Here you would typically process the content with TensorFlow or other methods
            # For simplicity, we will just use the content as is
            vector = process_document(content)  # Placeholder for actual processing logic
            # Upsert the document into Pinecone
            index.upsert([(file.filename, vector)])
            return jsonify({"message": "File uploaded and indexed successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "File upload failed"}), 500

def process_document(content):
    # Placeholder function for document processing
    # In a real scenario, you would convert the content to a vector using TensorFlow or other methods
    return [0.0] * 512  # Example: returning a dummy vector of zeros

if __name__ == '__main__':
    app.run(debug=True)