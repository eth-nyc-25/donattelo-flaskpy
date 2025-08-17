import requests
import json
import os

# API base URL
BASE_URL = "http://localhost:5000"

def test_health():
    """Test health check endpoint"""
    print("=== Testing Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_image_analysis():
    """Test image analysis and storage in Walrus"""
    print("=== Testing Image Analysis with Walrus ===")
    
    # Test image path
    test_image_path = "./test/img/image.png"
    
    if not os.path.exists(test_image_path):
        print(f"⚠️  Test image not found: {test_image_path}")
        print("Available test images:")
        test_dir = "./test/img"
        if os.path.exists(test_dir):
            for file in os.listdir(test_dir):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                    print(f"  - {test_dir}/{file}")
        print()
        return
    
    try:
        with open(test_image_path, 'rb') as f:
            files = {'image': f}
            
            response = requests.post(f"{BASE_URL}/analyze/image", files=files)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success! Image analyzed and stored in Walrus")
                print(f"📁 Image Blob ID: {result['image_blob_id']}")
                print(f"📁 Image Object ID: {result['image_object_id']}")
                print(f"🌐 Image URL: {result['image_url']}")
                print(f"📁 Metadata Blob ID: {result['metadata_blob_id']}")
                print(f"📁 Metadata Object ID: {result['metadata_object_id']}")
                print(f"📝 Metadata: {json.dumps(result['metadata'], indent=2)}")
                
                # Test downloading the image
                print("\n--- Testing Image Download ---")
                image_response = requests.get(f"{BASE_URL}/image/{result['image_blob_id']}")
                if image_response.status_code == 200:
                    print(f"✅ Image download successful (length: {len(image_response.content)} bytes)")
                else:
                    print(f"❌ Image download failed: {image_response.text}")
                
                # Test downloading the metadata
                print("\n--- Testing Metadata Download ---")
                metadata_response = requests.get(f"{BASE_URL}/metadata/{result['metadata_blob_id']}")
                if metadata_response.status_code == 200:
                    print(f"✅ Metadata download successful")
                    print(f"   Metadata: {json.dumps(metadata_response.json(), indent=2)}")
                else:
                    print(f"❌ Metadata download failed: {metadata_response.text}")
                    
            else:
                print(f"❌ Error: {response.json()}")
    except FileNotFoundError:
        print(f"❌ Image file not found: {test_image_path}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
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
    print("🚀 Testing Image Analyzer API with Walrus Storage")
    print("=" * 60)
    
    try:
        # Test health check
        test_health()
        
        # Test image analysis
        test_image_analysis()
        
        # Test other endpoints
        test_blobs_endpoint()
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the Flask server is running:")
        print("   python app.py")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()