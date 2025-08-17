import os
from dotenv import load_dotenv

load_dotenv()

# Walrus Configuration
WALRUS_PUBLISHER_URL = os.getenv("WALRUS_PUBLISHER_URL", "https://publisher.walrus-testnet.walrus.space")
WALRUS_AGGREGATOR_URL = os.getenv("WALRUS_AGGREGATOR_URL", "https://aggregator.walrus-testnet.walrus.space")
