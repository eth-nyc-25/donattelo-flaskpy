import google.generativeai as genai
from PIL import Image
import io
import base64
import json
import os
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

class GeminiSVGGenerator:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        # Create output directories
        os.makedirs("./output/svg", exist_ok=True)
        os.makedirs("./output/metadata", exist_ok=True)
    
    def generate_from_prompt(self, prompt: str) -> tuple[str, dict]:

        system_prompt = """
        Generate an SVG file based on the user's description. 
        Return ONLY the SVG code without any markdown formatting or explanations.
        Make it creative, visually appealing, and properly formatted SVG.
        """
        
        response = self.model.generate_content([system_prompt, prompt])
        svg_content = response.text.strip()
        
        # Clean up SVG content (remove markdown if present)
        if svg_content.startswith('```svg'):
            svg_content = svg_content.split('```svg')[1]
        if svg_content.endswith('```'):
            svg_content = svg_content.rsplit('```', 1)[0]
        svg_content = svg_content.strip()
        
        metadata = {
            "prompt": prompt,
            "type": "text_to_svg",
            "model": "gemini-1.5-flash",
            "generation_method": "prompt"
        }
        
        return svg_content, metadata
    
    def generate_from_image(self, image_path: str, prompt: str = "") -> tuple[str, dict]:

        try:
            with Image.open(image_path) as img:
                # Convert to base64 for Gemini
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                img_data = base64.b64encode(buffer.getvalue()).decode()
        except Exception as e:
            raise Exception(f"Failed to process image: {str(e)}")
        
        system_prompt = """
        Analyze this image and generate an SVG representation. 
        If a prompt is provided, incorporate those elements into the SVG.
        Return ONLY the SVG code without markdown formatting.
        Make the SVG creative and visually appealing.
        """
        
        if prompt:
            user_input = f"Image: {img_data}\nPrompt: {prompt}"
        else:
            user_input = f"Image: {img_data}"
        
        response = self.model.generate_content([system_prompt, user_input])
        svg_content = response.text.strip()
        
        # Clean up SVG content
        if svg_content.startswith('```svg'):
            svg_content = svg_content.split('```svg')[1]
        if svg_content.endswith('```'):
            svg_content = svg_content.rsplit('```', 1)[0]
        svg_content = svg_content.strip()
        
        metadata = {
            "image_path": image_path,
            "prompt": prompt,
            "type": "image_to_svg",
            "model": "gemini-1.5-flash",
            "generation_method": "image_analysis"
        }
        
        return svg_content, metadata
    
    def save_svg(self, svg_content: str, filename: str):
        """Save SVG content to ./output/svg directory"""
        # Ensure filename has .svg extension
        if not filename.endswith('.svg'):
            filename += '.svg'
        
        filepath = os.path.join("./output/svg", filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)
    
    def save_metadata(self, metadata: dict, filename: str):
        """Save metadata to ./output/metadata directory"""
        # Ensure filename has .json extension
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = os.path.join("./output/metadata", filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
    
    def save_generation(self, svg_content: str, metadata: dict, base_filename: str):
        """Save both SVG and metadata with same base filename"""
        self.save_svg(svg_content, base_filename)
        self.save_metadata(metadata, base_filename)
