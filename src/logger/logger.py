"""
Production Logging Module

This module configures the logging system for the entire project.

Author: Rishav Poddar
Project: AI Credit Risk Analysis Platform
"""

import logging
import os
from datetime import datetime

# -----------------------------
# Create logs directory
# -----------------------------

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

# -----------------------------
# Log file name
# -----------------------------

LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

# -----------------------------
# Configure logging
# -----------------------------

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(filename)s | %(message)s",

    handlers=[

        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler()

    ]

)
# Create logger object Every module can import and use the same logger.
logger = logging.getLogger(__name__)