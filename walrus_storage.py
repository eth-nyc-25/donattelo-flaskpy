from walrus import WalrusClient, WalrusAPIError
import json
import os
from dotenv import load_dotenv

class WalrusStorage:
    def __init__(self):
        load_dotenv()
        self.client = WalrusClient(
            publisher_base_url="https://publisher.walrus-testnet.walrus.space", 
            aggregator_base_url="https://aggregator.walrus-testnet.walrus.space"
        )
        self.bucket_name = os.getenv('WALRUS_BUCKET', 'images')

    def _extract_blob_info(self, response):
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

    def upload_image(self, image_data, metadata):
        """Upload image and its metadata to Walrus using publisher"""
        try:
            # Upload image data (without encoding_type to avoid HTTP 400 errors)
            image_response = self.client.put_blob(data=image_data)

            # Upload metadata
            metadata_json = json.dumps(metadata).encode('utf-8')
            metadata_response = self.client.put_blob(data=metadata_json)

            # Extract blob information from responses
            image_blob_id, image_object_id = self._extract_blob_info(image_response)
            metadata_blob_id, metadata_object_id = self._extract_blob_info(metadata_response)

            return {
                "image_blob_id": image_blob_id,
                "metadata_blob_id": metadata_blob_id,
                "image_object_id": image_object_id,
                "metadata_object_id": metadata_object_id
            }
        except WalrusAPIError as e:
            raise Exception(f"Walrus API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Upload failed: {str(e)}")

    def get_image_url(self, blob_id):
        """Get the URL for an image blob using aggregator for reading"""
        return f"https://aggregator.walrus-testnet.walrus.space/v1/blobs/{blob_id}"

    def download_image(self, blob_id):
        """Download image data from Walrus using aggregator"""
        try:
            return self.client.get_blob(blob_id)
        except WalrusAPIError as e:
            raise Exception(f"Walrus API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Download failed: {str(e)}")

    def download_metadata(self, blob_id):
        """Download and parse metadata from Walrus using aggregator"""
        try:
            metadata_bytes = self.client.get_blob(blob_id)
            return json.loads(metadata_bytes.decode('utf-8'))
        except WalrusAPIError as e:
            raise Exception(f"Walrus API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Metadata download failed: {str(e)}")

    def get_blob_metadata(self, blob_id):
        """Get blob metadata from Walrus using aggregator"""
        try:
            return self.client.get_blob_metadata(blob_id)
        except WalrusAPIError as e:
            raise Exception(f"Walrus API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Metadata retrieval failed: {str(e)}")
