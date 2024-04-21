import logging

# Configure the root logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define a custom logger if needed
logger = logging.getLogger(__name__)
