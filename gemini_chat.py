import google.generativeai as genai
import os
from dotenv import load_dotenv

class GeminiChat:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])
    
    def send_message(self, message: str, image_context: dict = None):
        """Send a message to Gemini with optional image context"""
        try:
            # If image context is provided, include it in the prompt
            if image_context:
                enhanced_message = f"""
                User message: {message}
                
                Image context:
                - Filename: {image_context.get('filename', 'N/A')}
                - Dimensions: {image_context.get('size', {}).get('width', 'N/A')}x{image_context.get('size', {}).get('height', 'N/A')}
                - Format: {image_context.get('format', 'N/A')}
                - File size: {image_context.get('file_size', 'N/A')} bytes
                - Walrus Blob ID: {image_context.get('blob_id', 'N/A')}
                - Image URL: {image_context.get('image_url', 'N/A')}
                """
                message = enhanced_message
            
            response = self.chat.send_message(message)
            return {
                "success": True,
                "response": response.text,
                "message_id": len(self.chat.history)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_chat_history(self):
        """Get the chat history"""
        return [
            {
                "role": msg.role,
                "content": msg.parts[0].text if msg.parts else ""
            }
            for msg in self.chat.history
        ]
