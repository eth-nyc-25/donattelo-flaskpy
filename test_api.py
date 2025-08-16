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
    """Test text-to-SVG generation with Walrus storage"""
    print("=== Testing Text-to-SVG Generation with Walrus ===")
    
    data = {
        "prompt": "A futuristic robot with glowing blue eyes and metallic armor"
    }
    
    response = requests.post(f"{BASE_URL}/generate/text", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success! Generated SVG stored in Walrus")
        print(f"📁 SVG Blob ID: {result['svg_blob_id']}")
        print(f"📁 SVG Object ID: {result['svg_object_id']}")
        print(f"🌐 SVG URL: {result['svg_url']}")
        print(f"📁 Metadata Blob ID: {result['metadata_blob_id']}")
        print(f"📁 Metadata Object ID: {result['metadata_object_id']}")
        print(f"📝 Metadata: {json.dumps(result['metadata'], indent=2)}")
        
        # Test downloading the SVG
        print("\n--- Testing SVG Download ---")
        svg_response = requests.get(f"{BASE_URL}/download/svg/{result['svg_blob_id']}")
        if svg_response.status_code == 200:
            print(f"✅ SVG download successful (length: {len(svg_response.text)} chars)")
        else:
            print(f"❌ SVG download failed: {svg_response.text}")
            
    else:
        print(f"❌ Error: {response.json()}")
    print()

def test_image_generation(image_path):
    """Test image-to-SVG generation with Walrus storage"""
    print("=== Testing Image-to-SVG Generation with Walrus ===")
    
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
                print(f"✅ Success! Generated SVG stored in Walrus")
                print(f"📁 SVG Blob ID: {result['svg_blob_id']}")
                print(f"📁 SVG Object ID: {result['svg_object_id']}")
                print(f"🌐 SVG URL: {result['svg_url']}")
                print(f"📁 Metadata Blob ID: {result['metadata_blob_id']}")
                print(f"📁 Metadata Object ID: {result['metadata_object_id']}")
                print(f"📝 Metadata: {json.dumps(result['metadata'], indent=2)}")
                
                # Test downloading the SVG
                print("\n--- Testing SVG Download ---")
                svg_response = requests.get(f"{BASE_URL}/download/svg/{result['svg_blob_id']}")
                if svg_response.status_code == 200:
                    print(f"✅ SVG download successful (length: {len(svg_response.text)} chars)")
                else:
                    print(f"❌ SVG download failed: {svg_response.text}")
                    
            else:
                print(f"❌ Error: {response.json()}")
    except FileNotFoundError:
        print(f"❌ Image file not found: {image_path}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    print()

def test_svg_url_endpoint():
    """Test getting SVG URL from blob ID"""
    print("=== Testing SVG URL Endpoint ===")
    
    # This would need a valid blob ID from a previous generation
    # For now, just test the endpoint structure
    test_blob_id = "test_blob_id"
    response = requests.get(f"{BASE_URL}/svg/{test_blob_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_blobs_endpoint():
    """Test blobs listing endpoint"""
    print("=== Testing Blobs Endpoint ===")
    response = requests.get(f"{BASE_URL}/blobs")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def main():
    """Run all tests"""
    print("🚀 Testing Gemini SVG Generator API with Walrus Storage")
    print("=" * 60)
    
    try:
        # Test health check
        test_health()
        
        # Test text generation
        test_text_generation()
        
        # Test image generation (if image exists)
        test_image_generation("input_image.jpg")  # Change this to your image path
        
        # Test other endpoints
        test_svg_url_endpoint()
        test_blobs_endpoint()
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the Flask server is running:")
        print("   python app.py")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()