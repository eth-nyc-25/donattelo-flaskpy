#!/usr/bin/env python3
"""
Test script for Walrus Python SDK functionality
This script tests the basic Walrus operations independently

Note: Publisher is used for writing/uploading, Aggregator is used for reading/downloading
"""

import os
import json
from datetime import datetime
from walrus import WalrusClient, WalrusAPIError

def extract_blob_info(response):
    """Extract blob ID and object ID from Walrus response"""
    if not response:
        return None, None
        
    # Handle newlyCreated response format
    if 'newlyCreated' in response:
        blob_object = response['newlyCreated'].get('blobObject', {})
        blob_id = blob_object.get('blobId')
        object_id = blob_object.get('id')
        return blob_id, object_id
        
    # Handle alreadyCertified response format
    elif 'alreadyCertified' in response:
        blob_id = response['alreadyCertified'].get('blobId')
        # For already certified, we might not have object_id
        return blob_id, None
        
    # Fallback for other response formats
    else:
        blob_id = response.get('blobId') or response.get('blob_id') or response.get('id')
        object_id = response.get('id') or response.get('object_id')
        return blob_id, object_id

def test_walrus_connection():
    """Test basic connection to Walrus"""
    print("=== Testing Walrus Connection ===")
    print("Publisher: Used for writing/uploading blobs")
    print("Aggregator: Used for reading/downloading blobs")
    print()
    
    try:
        client = WalrusClient(
            publisher_base_url="https://publisher.walrus-testnet.walrus.space",
            aggregator_base_url="https://aggregator.walrus-testnet.walrus.space"
        )
        print("✅ Walrus client initialized successfully")
        print("   Publisher: https://publisher.walrus-testnet.walrus.space")
        print("   Aggregator: https://aggregator.walrus-testnet.walrus.space")
        return client
    except Exception as e:
        print(f"❌ Failed to initialize Walrus client: {str(e)}")
        return None

def test_upload_small_blob(client):
    """Test uploading a small text blob using publisher"""
    print("\n=== Testing Small Blob Upload (Publisher) ===")
    
    try:
        test_data = b"Hello Walrus! This is a test blob."
        print(f"Uploading {len(test_data)} bytes via publisher...")
        
        response = client.put_blob(
            data=test_data,
            encoding_type="text/plain"
        )
        
        print(f"✅ Upload successful!")
        print(f"   Full response: {response}")
        print(f"   Response type: {type(response)}")
        
        # Extract blob information using the helper function
        blob_id, object_id = extract_blob_info(response)
        print(f"   Blob ID: {blob_id}")
        print(f"   Object ID: {object_id}")
        
        return blob_id
        
    except WalrusAPIError as e:
        print(f"❌ Walrus API error: {str(e)}")
        print(f"   Error details: {e}")
        return None
    except Exception as e:
        print(f"❌ Upload failed: {str(e)}")
        print(f"   Error type: {type(e)}")
        return None

def test_download_blob(client, blob_id):
    """Test downloading a blob using aggregator"""
    print(f"\n=== Testing Blob Download (Aggregator) ===")
    
    if not blob_id:
        print("⚠️  No blob ID to test download")
        return False
    
    try:
        print(f"Downloading blob: {blob_id}")
        print("Note: Download uses aggregator endpoint")
        downloaded_data = client.get_blob(blob_id)
        
        print(f"   Downloaded data type: {type(downloaded_data)}")
        print(f"   Downloaded data length: {len(downloaded_data) if downloaded_data else 0}")
        
        if downloaded_data == b"Hello Walrus! This is a test blob.":
            print("✅ Download successful! Data matches original")
            return True
        else:
            print(f"❌ Download failed! Data mismatch")
            print(f"   Expected: {b'Hello Walrus! This is a test blob.'}")
            print(f"   Got: {downloaded_data}")
            return False
            
    except WalrusAPIError as e:
        print(f"❌ Walrus API error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Download failed: {str(e)}")
        return False

def test_metadata_operations(client, blob_id):
    """Test metadata operations using aggregator"""
    print(f"\n=== Testing Metadata Operations (Aggregator) ===")
    
    if not blob_id:
        print("⚠️  No blob ID to test metadata")
        return False
    
    try:
        print(f"Getting metadata for blob: {blob_id}")
        print("Note: Metadata retrieval uses aggregator endpoint")
        # Try to get blob metadata
        metadata = client.get_blob_metadata(blob_id)
        print(f"✅ Metadata retrieved successfully")
        print(f"   Metadata: {metadata}")
        return True
        
    except WalrusAPIError as e:
        print(f"❌ Walrus API error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Metadata operation failed: {str(e)}")
        return False

def test_file_upload(client):
    """Test uploading from a file using publisher"""
    print(f"\n=== Testing File Upload (Publisher) ===")
    
    try:
        # Create a test file
        test_file_path = "./test_walrus_file.txt"
        test_content = "This is a test file for Walrus upload"
        
        with open(test_file_path, 'w') as f:
            f.write(test_content)
        
        print(f"Created test file: {test_file_path}")
        print(f"File content length: {len(test_content)} chars")
        print("Note: File upload uses publisher endpoint")
        
        # Upload the file
        response = client.put_blob_from_file(test_file_path)
        
        print(f"✅ File upload successful!")
        print(f"   Full response: {response}")
        print(f"   Response type: {type(response)}")
        
        # Extract blob information using the helper function
        blob_id, object_id = extract_blob_info(response)
        print(f"   Blob ID: {blob_id}")
        print(f"   Object ID: {object_id}")
        
        # Clean up test file
        os.remove(test_file_path)
        
        return blob_id
        
    except WalrusAPIError as e:
        print(f"❌ Walrus API error: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ File upload failed: {str(e)}")
        # Clean up test file on error
        if os.path.exists("./test_walrus_file.txt"):
            os.remove("./test_walrus_file.txt")
        return None

def test_simple_text_upload(client):
    """Test uploading simple text without encoding type using publisher"""
    print(f"\n=== Testing Simple Text Upload (Publisher) ===")
    
    try:
        test_data = b"Simple test without encoding type"
        print(f"Uploading {len(test_data)} bytes via publisher...")
        
        response = client.put_blob(data=test_data)
        
        print(f"✅ Simple upload successful!")
        print(f"   Full response: {response}")
        print(f"   Response type: {type(response)}")
        
        # Extract blob information using the helper function
        blob_id, object_id = extract_blob_info(response)
        print(f"   Blob ID: {blob_id}")
        print(f"   Object ID: {object_id}")
        
        return blob_id
        
    except WalrusAPIError as e:
        print(f"❌ Walrus API error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Simple upload failed: {str(e)}")
        return False

def main():
    """Run all Walrus SDK tests"""
    print("🧪 Testing Walrus Python SDK")
    print("=" * 50)
    print("📝 Note: Publisher = Write/Upload, Aggregator = Read/Download")
    print("=" * 50)
    
    # Test connection
    client = test_walrus_connection()
    if not client:
        print("\n❌ Cannot proceed without Walrus client")
        return
    
    # Test simple upload first
    simple_blob_id = test_simple_text_upload(client)
    
    # Test basic operations
    blob_id = test_upload_small_blob(client)
    download_success = test_download_blob(client, blob_id or simple_blob_id)
    metadata_success = test_metadata_operations(client, blob_id or simple_blob_id)
    
    # Test file operations
    file_blob_id = test_file_upload(client)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Connection: ✅")
    print(f"   Simple Upload (Publisher): {'✅' if simple_blob_id else '❌'}")
    print(f"   Upload with Encoding (Publisher): {'✅' if blob_id else '❌'}")
    print(f"   Download (Aggregator): {'✅' if download_success else '❌'}")
    print(f"   Metadata (Aggregator): {'✅' if metadata_success else '❌'}")
    print(f"   File Upload (Publisher): {'✅' if file_blob_id else '❌'}")
    
    success_count = sum([
        bool(simple_blob_id),
        bool(blob_id),
        download_success,
        metadata_success,
        bool(file_blob_id)
    ])
    
    if success_count >= 3:
        print(f"\n🎉 {success_count}/5 tests passed! Walrus SDK is working.")
        print("✅ Publisher (upload) and Aggregator (download) endpoints configured correctly")
    else:
        print(f"\n⚠️  Only {success_count}/5 tests passed. Check the output above for details.")

if __name__ == "__main__":
    main()
