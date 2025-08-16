from flask import Flask, request, jsonify, send_file
from gemini_svg_generator import GeminiSVGGenerator
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize generator
generator = GeminiSVGGenerator()

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Gemini SVG Generator"})

@app.route('/generate/text', methods=['POST'])
def generate_from_text():
    """Generate SVG from text prompt"""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing 'prompt' field"}), 400
        
        prompt = data['prompt']
        if not prompt.strip():
            return jsonify({"error": "Prompt cannot be empty"}), 400
        
        # Generate SVG and metadata
        svg_content, metadata = generator.generate_from_prompt(prompt)
        
        # Generate unique filename
        filename = f"text_generated_{uuid.uuid4().hex[:8]}"
        
        # Save files
        generator.save_generation(svg_content, metadata, filename)
        
        # Return response with file paths
        response = {
            "success": True,
            "filename": filename,
            "svg_url": f"/download/svg/{filename}.svg",
            "metadata_url": f"/download/metadata/{filename}.json",
            "metadata": metadata
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate/image', methods=['POST'])
def generate_from_image():
    """Generate SVG from uploaded image"""
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
            
            # Generate unique filename
            filename = f"image_generated_{uuid.uuid4().hex[:8]}"
            
            # Save files
            generator.save_generation(svg_content, metadata, filename)
            
            # Clean up temp file
            os.remove(temp_path)
            
            # Return response
            response = {
                "success": True,
                "filename": filename,
                "svg_url": f"/download/svg/{filename}.svg",
                "metadata_url": f"/download/metadata/{filename}.json",
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

@app.route('/download/svg/<filename>', methods=['GET'])
def download_svg(filename):
    """Download SVG file"""
    try:
        filepath = os.path.join("./output/svg", filename)
        if not os.path.exists(filepath):
            return jsonify({"error": "File not found"}), 404
        
        return send_file(filepath, mimetype='image/svg+xml')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/metadata/<filename>', methods=['GET'])
def download_metadata(filename):
    """Download metadata file"""
    try:
        filepath = os.path.join("./output/metadata", filename)
        if not os.path.exists(filepath):
            return jsonify({"error": "File not found"}), 404
        
        return send_file(filepath, mimetype='application/json')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/files', methods=['GET'])
def list_files():
    """List all generated files"""
    try:
        svg_files = []
        metadata_files = []
        
        # Get SVG files
        svg_dir = "./output/svg"
        if os.path.exists(svg_dir):
            for file in os.listdir(svg_dir):
                if file.endswith('.svg'):
                    svg_files.append({
                        "filename": file,
                        "download_url": f"/download/svg/{file}"
                    })
        
        # Get metadata files
        metadata_dir = "./output/metadata"
        if os.path.exists(metadata_dir):
            for file in os.listdir(metadata_dir):
                if file.endswith('.json'):
                    metadata_files.append({
                        "filename": file,
                        "download_url": f"/download/metadata/{file}"
                    })
        
        return jsonify({
            "svg_files": svg_files,
            "metadata_files": metadata_files,
            "total_files": len(svg_files)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
