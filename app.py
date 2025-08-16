from flask import Flask, request, jsonify, send_file
from gemini_svg_generator import GeminiSVGGenerator
from walrus_storage import WalrusStorage
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize generator and storage
generator = GeminiSVGGenerator()
walrus_storage = WalrusStorage()

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Gemini SVG Generator with Walrus Storage"})

@app.route('/generate/text', methods=['POST'])
def generate_from_text():
    """Generate SVG from text prompt and store in Walrus"""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing 'prompt' field"}), 400
        
        prompt = data['prompt']
        if not prompt.strip():
            return jsonify({"error": "Prompt cannot be empty"}), 400
        
        # Generate SVG and metadata
        svg_content, metadata = generator.generate_from_prompt(prompt)
        
        # Upload to Walrus storage
        upload_result = walrus_storage.upload_svg(svg_content, metadata)
        
        # Get SVG URL
        svg_url = walrus_storage.get_svg_url(upload_result["svg_blob_id"])
        
        # Return response with Walrus info
        response = {
            "success": True,
            "svg_blob_id": upload_result["svg_blob_id"],
            "svg_object_id": upload_result["svg_object_id"],
            "svg_url": svg_url,
            "metadata_blob_id": upload_result["metadata_blob_id"],
            "metadata_object_id": upload_result["metadata_object_id"],
            "metadata": upload_result["metadata"]
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate/image', methods=['POST'])
def generate_from_image():
    """Generate SVG from uploaded image and store in Walrus"""
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No image file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Allowed: " + ", ".join(ALLOWED_EXTENSIONS)}), 400
        
        # Get optional prompt
        prompt = request.form.get('prompt', '')
        
        # Save uploaded image temporarily
        temp_filename = f"temp_{uuid.uuid4().hex[:8]}_{secure_filename(file.filename)}"
        temp_path = os.path.join("./temp", temp_filename)
        os.makedirs("./temp", exist_ok=True)
        file.save(temp_path)
        
        try:
            # Generate SVG from image
            svg_content, metadata = generator.generate_from_image(temp_path, prompt)
            
            # Upload to Walrus storage
            upload_result = walrus_storage.upload_svg(svg_content, metadata)
            
            # Get SVG URL
            svg_url = walrus_storage.get_svg_url(upload_result["svg_blob_id"])
            
            # Clean up temp file
            os.remove(temp_path)
            
            # Return response with Walrus info
            response = {
                "success": True,
                "svg_blob_id": upload_result["svg_blob_id"],
                "svg_object_id": upload_result["svg_object_id"],
                "svg_url": svg_url,
                "metadata_blob_id": upload_result["metadata_blob_id"],
                "metadata_object_id": upload_result["metadata_object_id"],
                "metadata": upload_result["metadata"]
            }
            
            return jsonify(response), 200
            
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/svg/<blob_id>', methods=['GET'])
def download_svg(blob_id):
    """Download SVG from Walrus by blob ID"""
    try:
        svg_content = walrus_storage.download_svg(blob_id)
        return svg_content, 200, {'Content-Type': 'image/svg+xml'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/metadata/<blob_id>', methods=['GET'])
def download_metadata(blob_id):
    """Download metadata from Walrus by blob ID"""
    try:
        metadata = walrus_storage.download_metadata(blob_id)
        return jsonify(metadata), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/svg/<blob_id>', methods=['GET'])
def get_svg_url(blob_id):
    """Get SVG URL from Walrus blob ID"""
    try:
        svg_url = walrus_storage.get_svg_url(blob_id)
        return jsonify({
            "blob_id": blob_id,
            "svg_url": svg_url
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/blobs', methods=['GET'])
def list_blobs():
    """List all blobs in Walrus (placeholder)"""
    try:
        # Note: Current Walrus SDK doesn't have a list method
        # This is a placeholder for future implementation
        return jsonify({
            "message": "Blob listing not yet implemented in current Walrus SDK",
            "suggestion": "Use individual blob IDs from generation responses"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)