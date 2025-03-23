"""
Logging utility for the AI Dubbing project.
This module sets up a centralized logging system that writes to both console and file.
"""

import logging
import sys
import os
from datetime import datetime
from config.settings import LOGS_DIR, LOG_LEVEL, LOG_FILE

# ANSI color codes for colored console output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to log levels in console output."""
    
    COLORS = {
        'DEBUG': Colors.BLUE,
        'INFO': Colors.GREEN,
        'WARNING': Colors.YELLOW,
        'ERROR': Colors.RED,
        'CRITICAL': Colors.BG_RED + Colors.WHITE + Colors.BOLD
    }
    
    def format(self, record):
        # Get the original formatted message
        log_message = super().format(record)
        
        # Apply color to the level name if available
        if record.levelname in self.COLORS:
            color_code = self.COLORS[record.levelname]
            colored_levelname = f"{color_code}{record.levelname}{Colors.RESET}"
            log_message = log_message.replace(record.levelname, colored_levelname, 1)
            
        return log_message

def setup_logger(name):
    """
    Set up a logger with the given name that logs to both console and file.
    
    Args:
        name (str): Name of the logger, typically __name__ from the calling module
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Set level based on config
    level = getattr(logging, LOG_LEVEL)
    logger.setLevel(level)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s - %(name)s - %(message)s'
    )
    console_formatter = ColoredFormatter(
        '%(levelname)s: %(message)s'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Create file handler
    os.makedirs(LOGS_DIR, exist_ok=True)
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    return logger


# Example usage
if __name__ == "__main__":
    logger = setup_logger(__name__)
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message") 