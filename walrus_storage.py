from walrus import WalrusClient, WalrusAPIError
from config import WALRUS_PUBLISHER_URL, WALRUS_AGGREGATOR_URL
import json
import os

class WalrusStorage:
    def __init__(self):
        self.client = WalrusClient(
            publisher_base_url=WALRUS_PUBLISHER_URL,
            aggregator_base_url=WALRUS_AGGREGATOR_URL
        )
    
    def upload_svg(self, svg_content: str, metadata: dict) -> dict:
        """Upload SVG to Walrus and return blob info"""
        try:
            # Convert SVG string to bytes
            svg_bytes = svg_content.encode('utf-8')
            
            # Upload SVG to Walrus
            svg_response = self.client.put_blob(
                data=svg_bytes,
                encoding_type="utf-8",
                epochs=1,
                deletable=False
            )
            
            # Add SVG blob info to metadata
            metadata["svg_blob_id"] = svg_response.get("blob_id")
            metadata["svg_object_id"] = svg_response.get("object_id")
            
            # Convert metadata to JSON string and upload
            metadata_json = json.dumps(metadata, indent=2)
            metadata_bytes = metadata_json.encode('utf-8')
            
            metadata_response = self.client.put_blob(
                data=metadata_bytes,
                encoding_type="utf-8",
                epochs=1,
                deletable=False
            )
            
            # Add metadata blob info
            metadata["metadata_blob_id"] = metadata_response.get("blob_id")
            metadata["metadata_object_id"] = metadata_response.get("object_id")
            
            # Return complete response
            return {
                "success": True,
                "svg_blob_id": svg_response.get("blob_id"),
                "svg_object_id": svg_response.get("object_id"),
                "metadata_blob_id": metadata_response.get("blob_id"),
                "metadata_object_id": metadata_response.get("object_id"),
                "metadata": metadata
            }
            
        except WalrusAPIError as e:
            raise Exception(f"Walrus API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to upload to Walrus: {str(e)}")
    
    def get_svg_url(self, blob_id: str) -> str:
        """Get SVG URL from blob ID"""
        try:
            # Get blob metadata to construct URL
            metadata = self.client.get_blob_metadata(blob_id)
            # Construct URL based on Walrus structure
            return f"{WALRUS_AGGREGATOR_URL}/blob/{blob_id}"
        except WalrusAPIError as e:
            raise Exception(f"Failed to get SVG URL: {str(e)}")
    
    def download_svg(self, blob_id: str) -> str:
        """Download SVG content from blob ID"""
        try:
            svg_bytes = self.client.get_blob(blob_id)
            return svg_bytes.decode('utf-8')
        except WalrusAPIError as e:
            raise Exception(f"Failed to download SVG: {str(e)}")
    
    def download_metadata(self, blob_id: str) -> dict:
        """Download metadata from blob ID"""
        try:
            metadata_bytes = self.client.get_blob(blob_id)
            return json.loads(metadata_bytes.decode('utf-8'))
        except WalrusAPIError as e:
            raise Exception(f"Failed to download metadata: {str(e)}")
    
    def list_blobs(self) -> list:
        """List all blobs (basic implementation)"""
        # Note: This is a placeholder as the current SDK doesn't have a list method
        # You might need to implement this differently based on your needs
        return []
