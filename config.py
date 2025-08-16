import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Walrus Configuration
WALRUS_PUBLISHER_URL = os.getenv("WALRUS_PUBLISHER_URL", "https://publisher.walrus-testnet.walrus.space")
WALRUS_AGGREGATOR_URL = os.getenv("WALRUS_AGGREGATOR_URL", "https://aggregator.walrus-testnet.walrus.space")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")
