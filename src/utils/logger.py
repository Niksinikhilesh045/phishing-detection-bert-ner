"""
Centralized logging configuration for the Phishing Detection System
"""

import logging
import logging.config
import os
import sys
from pathlib import Path
from typing import Optional
import structlog
from rich.logging import RichHandler
from rich.console import Console

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    use_rich: bool = True,
    json_logs: bool = False
) -> None:
    """
    Set up logging configuration for the entire application
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path. If None, uses default log file
        use_rich: Whether to use Rich for colored console output
        json_logs: Whether to use JSON formatting for structured logs
    """
    
    # Default log file
    if log_file is None:
        log_file = LOGS_DIR / "phishing_detection.log"
    
    # Configure structlog for structured logging
    if json_logs:
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

    # Logging configuration
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "simple": {
                "format": "%(levelname)s - %(name)s - %(message)s"
            },
            "json": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
            },
        },
        "handlers": {
            "console": {
                "class": "rich.logging.RichHandler" if use_rich else "logging.StreamHandler",
                "level": level,
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "json" if json_logs else "detailed",
                "filename": str(log_file),
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8"
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "json" if json_logs else "detailed",
                "filename": str(LOGS_DIR / "errors.log"),
                "maxBytes": 10485760,  # 10MB
                "backupCount": 3,
                "encoding": "utf8"
            }
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["console", "file"],
                "level": level,
                "propagate": False
            },
            "phishing_detection": {
                "handlers": ["console", "file", "error_file"],
                "level": level,
                "propagate": False
            },
            # Third-party loggers
            "transformers": {
                "level": "WARNING",
                "propagate": True
            },
            "urllib3": {
                "level": "WARNING",
                "propagate": True
            },
            "requests": {
                "level": "WARNING", 
                "propagate": True
            }
        }
    }
    
    # Apply configuration
    logging.config.dictConfig(config)
    
    # Set up Rich console if using Rich handler
    if use_rich:
        console = Console()
        console.print(f"[green]✓[/green] Logging configured - Level: {level}")
        if log_file:
            console.print(f"[green]✓[/green] Log file: {log_file}")


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance with the specified name
    
    Args:
        name: Logger name (typically __name__)
        level: Optional logging level override
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if level:
        logger.setLevel(getattr(logging, level.upper()))
    
    return logger


def log_system_info() -> None:
    """Log system information for debugging"""
    import platform
    import torch
    import transformers
    
    logger = get_logger(__name__)
    
    logger.info("=== System Information ===")
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"PyTorch version: {torch.__version__}")
    logger.info(f"Transformers version: {transformers.__version__}")
    logger.info(f"CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        logger.info(f"CUDA device: {torch.cuda.get_device_name()}")
        logger.info(f"CUDA version: {torch.version.cuda}")


def setup_ml_logging() -> None:
    """Set up logging for ML experiments"""
    import warnings
    
    # Suppress common ML library warnings
    warnings.filterwarnings("ignore", category=UserWarning, module="transformers")
    warnings.filterwarnings("ignore", category=FutureWarning, module="transformers")
    warnings.filterwarnings("ignore", category=UserWarning, module="torch")
    
    # Set specific loggers to appropriate levels
    logging.getLogger("transformers").setLevel(logging.WARNING)
    logging.getLogger("torch").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


# Initialize logging when module is imported
if not logging.getLogger().handlers:
    # Check for environment variables
    log_level = os.getenv("LOG_LEVEL", "INFO")
    use_json_logs = os.getenv("JSON_LOGS", "false").lower() == "true"
    use_rich_logs = os.getenv("RICH_LOGS", "true").lower() == "true"
    
    setup_logging(
        level=log_level,
        use_rich=use_rich_logs,
        json_logs=use_json_logs
    )
    
    setup_ml_logging()


# Example usage functions
def example_logging():
    """Example of how to use the logging system"""
    logger = get_logger(__name__)
    
    logger.debug("This is a debug message")
    logger.info("Starting email analysis")
    logger.warning("Large model detected - may use significant memory")
    logger.error("Failed to load email file")
    
    # Structured logging with extra context
    logger.info("Processing email", extra={
        "email_id": "12345",
        "sender": "example@domain.com", 
        "confidence": 0.95
    })


if __name__ == "__main__":
    # Demo the logging system
    example_logging()
    log_system_info()