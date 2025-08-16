import requests
import json

# API base URL
BASE_URL = "http://localhost:5000"

def test_health():
    """Test health check endpoint"""
    print("=== Testing Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_text_generation():
    """Test text-to-SVG generation"""
    print("=== Testing Text-to-SVG Generation ===")
    
    data = {
        "prompt": "A futuristic robot with glowing blue eyes and metallic armor"
    }
    
    response = requests.post(f"{BASE_URL}/generate/text", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success! Generated: {result['filename']}")
        print(f"📁 SVG URL: {result['svg_url']}")
        print(f"📁 Metadata URL: {result['metadata_url']}")
        print(f"📝 Metadata: {json.dumps(result['metadata'], indent=2)}")
    else:
        print(f"❌ Error: {response.json()}")
    print()

def test_image_generation(image_path):
    """Test image-to-SVG generation"""
    print("=== Testing Image-to-SVG Generation ===")
    
    if not image_path or not image_path.strip():
        print("⚠️  No image path provided, skipping image test")
        print()
        return
    
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            data = {'prompt': 'Make it more colorful and add magical elements'}
            
            response = requests.post(f"{BASE_URL}/generate/image", files=files, data=data)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success! Generated: {result['filename']}")
                print(f"📁 SVG URL: {result['svg_url']}")
                print(f"📁 Metadata URL: {result['metadata_url']}")
                print(f"📝 Metadata: {json.dumps(result['metadata'], indent=2)}")
            else:
                print(f"❌ Error: {response.json()}")
    except FileNotFoundError:
        print(f"❌ Image file not found: {image_path}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    print()

def test_list_files():
    """Test file listing endpoint"""
    print("=== Testing File Listing ===")
    response = requests.get(f"{BASE_URL}/files")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"📁 Total files: {result['total_files']}")
        print(f"📁 SVG files: {len(result['svg_files'])}")
        print(f"📁 Metadata files: {len(result['metadata_files'])}")
        
        if result['svg_files']:
            print("📁 SVG files:")
            for file in result['svg_files']:
                print(f"   - {file['filename']}")
    else:
        print(f"❌ Error: {response.json()}")
    print()

def main():
    """Run all tests"""
    print("🚀 Testing Gemini SVG Generator API")
    print("=" * 50)
    
    try:
        # Test health check
        test_health()
        
        # Test text generation
        test_text_generation()
        
        # Test image generation (if image exists)
        test_image_generation("input_image.jpg")  # Change this to your image path
        
        # Test file listing
        test_list_files()
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the Flask server is running:")
        print("   python app.py")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
