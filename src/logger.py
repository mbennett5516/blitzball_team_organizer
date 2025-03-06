import logging

# Configure the logger once, at the module level
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Create a single logger instance
logger = logging.getLogger("blitzball")
