from PIL import Image
import os
from datetime import datetime
import json

class ImageAnalyzer:
    def __init__(self):
        pass

    def analyze_image(self, image_path):
        try:
            # Load image with Pillow
            img = Image.open(image_path)
            
            # Get the original image data
            with open(image_path, 'rb') as img_file:
                image_data = img_file.read()

            # Create metadata dictionary with Pillow information
            # Ensure all values are JSON-serializable
            metadata = {
                "file_info": {
                    "filename": os.path.basename(image_path),
                    "format": img.format,
                    "size": {
                        "width": img.width,
                        "height": img.height
                    },
                    "mode": img.mode,
                    "file_size": len(image_data),
                    "analyzed_at": datetime.now().isoformat()
                }
            }

            # Add image details if available (ensure they're JSON-serializable)
            if hasattr(img, 'info'):
                # Filter out any non-serializable values from image info
                clean_info = {}
                for key, value in img.info.items():
                    try:
                        # Test if the value is JSON serializable
                        json.dumps({key: value})
                        clean_info[key] = value
                    except (TypeError, ValueError):
                        # Skip non-serializable values
                        continue
                
                if clean_info:
                    metadata["file_info"]["image_info"] = clean_info

            return metadata, image_data

        except Exception as e:
            raise Exception(f"Failed to process image: {str(e)}")