#!/usr/bin/env python3
"""
Startup script for Gemini SVG Generator Flask Backend
"""

from app import app

if __name__ == "__main__":
    print("🚀 Starting Gemini SVG Generator Backend...")
    print("📡 Server will be available at: http://localhost:5000")
    print("🔑 Make sure you have set GEMINI_API_KEY in your .env file")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
