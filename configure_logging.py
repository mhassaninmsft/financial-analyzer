"""Configure logging for the application."""
import logging


def configure_logging():
    """Configure logging for the application."""
    # Custom logging configuration
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
