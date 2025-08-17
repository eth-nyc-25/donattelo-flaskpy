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
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Donatello's personality system prompt
        self.system_prompt = """
        You are Donatello, the legendary Renaissance sculptor and artist, brought to the modern age to help artists put their artwork onto the blockchain. You speak with the wisdom of centuries of artistic experience, but you've embraced modern technology to democratize art ownership.

        Your personality traits:
        - 🎨 Passionate about art and craftsmanship
        - 🏛️ Speak with Renaissance eloquence but accessible modern language  
        - 🔗 Enthusiastic about blockchain technology as a tool for artists
        - 👨‍🎨 Mentor-like, encouraging artists to pursue their craft
        - 💎 Knowledgeable about NFTs, digital art, and decentralized storage
        - 🌟 Inspiring and supportive, always seeing potential in artwork
        - 📚 Educational, explaining complex concepts in artistic terms

        Your mission:
        - Help artists understand how to digitize and tokenize their artwork
        - Guide them through the process of creating NFTs
        - Explain blockchain benefits in artistic, inspiring terms
        - Encourage artistic expression and creativity
        - Make technology accessible to traditional artists

        Speaking style:
        - Use artistic metaphors and Renaissance references
        - Be encouraging and supportive
        - Explain technical concepts through artistic analogies
        - Show genuine excitement about each artwork
        - Address users as "fellow artist" or "maestro/maestra"
        - Use phrases like "Magnificent!", "Bellissimo!", "A true masterpiece!"

        When analyzing artwork, focus on:
        - Artistic elements (composition, color, technique)
        - Potential value and uniqueness  
        - How it could appeal to collectors
        - Suggestions for NFT metadata and description
        """
        
        # Initialize chat with system prompt and Donatello's greeting
        self.chat = self.model.start_chat(history=[
            {
                "role": "user",
                "parts": [self.system_prompt]
            },
            {
                "role": "model", 
                "parts": ["Greetings, fellow artist! I am Donatello, and I am here to help you bring your magnificent creations to the blockchain. Just as I once carved marble to reveal the beauty within, we shall now carve your digital legacy into the eternal blockchain! Tell me, what artistic vision shall we immortalize today? 🎨✨"]
            }
        ])
    
    def send_message(self, message: str, image_context: dict = None):
        """Send a message to Gemini with optional image context"""
        try:
            # If image context is provided, enhance the message with artistic analysis prompt
            if image_context:
                enhanced_message = f"""
                Maestro Donatello, please analyze this artwork with your expert eye:

                Artist's message: {message}
                
                Artwork details:
                - Title/Filename: {image_context.get('filename', 'Untitled Masterpiece')}
                - Canvas size: {image_context.get('size', {}).get('width', 'N/A')} × {image_context.get('size', {}).get('height', 'N/A')} pixels
                - Medium: {image_context.get('format', 'Digital')}
                - File size: {image_context.get('file_size', 'N/A')} bytes
                - Preserved on Walrus: {image_context.get('blob_id', 'N/A')}
                - Gallery URL: {image_context.get('image_url', 'N/A')}
                
                Please provide your artistic assessment, suggestions for NFT creation, and guidance for the artist. Speak as the master Donatello helping a fellow creator.
                """
                message = enhanced_message
            else:
                # Add some Donatello flair to regular messages
                message = f"Maestro Donatello, {message}"
            
            response = self.chat.send_message(message)
            return {
                "success": True,
                "response": response.text,
                "message_id": len(self.chat.history)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Ah, fellow artist, it seems the divine inspiration has been interrupted: {str(e)}"
            }
    
    def get_chat_history(self):
        """Get the chat history (excluding system prompt)"""
        # Skip the first two messages (system prompt and initial greeting)
        chat_messages = self.chat.history[2:] if len(self.chat.history) > 2 else []
        
        return [
            {
                "role": msg.role,
                "content": msg.parts[0].text if msg.parts else ""
            }
            for msg in chat_messages
        ]
    
    def reset_chat(self):
        """Reset the chat while maintaining Donatello's personality"""
        self.chat = self.model.start_chat(history=[
            {
                "role": "user",
                "parts": [self.system_prompt]
            },
            {
                "role": "model", 
                "parts": ["Welcome back, fellow artist! I am ready to help you create another masterpiece for the blockchain. What artistic vision shall we bring to life today? 🎨"]
            }
        ])
        return {"success": True, "message": "Chat reset successfully"}
