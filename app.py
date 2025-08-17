from flask import Flask, request, jsonify, send_file
from image_analyzer import ImageAnalyzer
from walrus_storage import WalrusStorage
from gemini_chat import GeminiChat
import os
import uuid
from werkzeug.utils import secure_filename
import io
from flask_cors import CORS

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure CORS to allow requests from your Next.js frontend
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"], 
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"])

# Initialize services
analyzer = ImageAnalyzer()
walrus_storage = WalrusStorage()
gemini_chat = GeminiChat()

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Image Analyzer with Walrus Storage"})

@app.route('/chat', methods=['POST'])
def chat_with_gemini():
    """Chat with Gemini AI"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        image_context = data.get('image_context', None)
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        result = gemini_chat.send_message(message, image_context)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat/history', methods=['GET'])
def get_chat_history():
    """Get chat history"""
    try:
        history = gemini_chat.get_chat_history()
        return jsonify({"history": history}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analyze/image', methods=['POST'])
def analyze_image():
    """Analyze image and store result in Walrus"""
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No image file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Allowed: " + ", ".join(ALLOWED_EXTENSIONS)}), 400
        
        # Save uploaded image temporarily
        temp_filename = f"temp_{uuid.uuid4().hex[:8]}_{secure_filename(file.filename)}"
        temp_path = os.path.join("./temp", temp_filename)
        os.makedirs("./temp", exist_ok=True)
        file.save(temp_path)
        
        try:
            # Analyze image and get metadata
            metadata, image_data = analyzer.analyze_image(temp_path)
            
            # Upload to Walrus storage
            upload_result = walrus_storage.upload_image(image_data, metadata)
            
            # Get image URL
            image_url = walrus_storage.get_image_url(upload_result["image_blob_id"])
            
            # Clean up temp file
            os.remove(temp_path)
            
            # Return response with Walrus info
            response = {
                "success": True,
                "image_url": image_url,
                "image_blob_id": upload_result["image_blob_id"],
                "metadata_blob_id": upload_result["metadata_blob_id"],
                "image_object_id": upload_result["image_object_id"],
                "metadata_object_id": upload_result["metadata_object_id"],
                "metadata": metadata
            }
            
            return jsonify(response), 200
            
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/image/<blob_id>', methods=['GET'])
def get_image(blob_id):
    """Download image from Walrus by blob ID"""
    try:
        image_data = walrus_storage.download_image(blob_id)
        return send_file(
            io.BytesIO(image_data),
            mimetype='image/*'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/metadata/<blob_id>', methods=['GET'])
def get_metadata(blob_id):
    """Download metadata from Walrus by blob ID"""
    try:
        metadata = walrus_storage.download_metadata(blob_id)
        return jsonify(metadata), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/blobs', methods=['GET'])
def list_blobs():
    """List all blobs (placeholder - would need Walrus SDK support for listing)"""
    try:
        # This is a placeholder - the Walrus SDK doesn't currently support listing blobs
        # You would need to maintain your own database of uploaded blobs
        return jsonify({
            "message": "Blob listing not yet implemented",
            "note": "The Walrus SDK doesn't currently support listing all blobs",
            "suggestion": "Maintain your own database of uploaded blob IDs"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
