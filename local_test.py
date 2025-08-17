from image_analyzer import ImageAnalyzer
from walrus_storage import WalrusStorage
import json
import os
from datetime import datetime

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.hex()
        return super().default(obj)

def test_image_analysis_and_storage():
    # Initialize services
    analyzer = ImageAnalyzer()
    storage = WalrusStorage()
    
    # Test image path
    test_image_path = "./test/img/image.png"
    
    try:
        print(f"\n=== Image Analysis Test ===")
        print(f"Started at: {datetime.now().isoformat()}")
        print(f"Testing image: {test_image_path}")

        # Step 1: Analyze image
        print("\n1. Analyzing image...")
        metadata, image_data = analyzer.analyze_image(test_image_path)
        
        print("\nImage metadata:")
        print(json.dumps(metadata, indent=2, cls=CustomJSONEncoder))
        print(f"Image data size: {len(image_data)} bytes")
        
        # Step 2: Upload to Walrus
        print("\n2. Uploading to Walrus storage...")
        upload_result = storage.upload_image(image_data, metadata)
        
        # Step 3: Get image URL
        print("\n3. Getting image URL...")
        image_url = storage.get_image_url(upload_result["image_blob_id"])
        
        # Prepare result
        result = {
            "success": True,
            "test_timestamp": datetime.now().isoformat(),
            "image_path": test_image_path,
            "image_url": image_url,
            "image_blob_id": upload_result["image_blob_id"],
            "metadata_blob_id": upload_result["metadata_blob_id"],
            "image_object_id": upload_result["image_object_id"],
            "metadata_object_id": upload_result["metadata_object_id"],
            "metadata": metadata
        }
        
        # Print success info
        print("\n=== Test Results ===")
        print(f"✓ Image analyzed successfully")
        print(f"✓ Uploaded to Walrus")
        print(f"✓ Image URL: {image_url}")
        print(f"✓ Image Blob ID: {upload_result['image_blob_id']}")
        print(f"✓ Metadata Blob ID: {upload_result['metadata_blob_id']}")
        print(f"✓ Image Object ID: {upload_result['image_object_id']}")
        print(f"✓ Metadata Object ID: {upload_result['metadata_object_id']}")
        
        return result
        
    except Exception as e:
        error_result = {
            "success": False,
            "test_timestamp": datetime.now().isoformat(),
            "error": str(e)
        }
        print(f"\n❌ Error: {str(e)}")
        return error_result

if __name__ == "__main__":
    # Ensure test directories exist
    os.makedirs("./test/img", exist_ok=True)
    os.makedirs("./test/results", exist_ok=True)
    
    # Run test
    result = test_image_analysis_and_storage()
    
    # Save results with custom encoder
    result_file = f"./test/results/test_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(result_file, "w") as f:
        json.dump(result, f, indent=2, cls=CustomJSONEncoder)
    
    print(f"\nTest results saved to: {result_file}")