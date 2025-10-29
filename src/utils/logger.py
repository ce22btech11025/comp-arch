import logging
import os
import yaml

def get_logger(name: str = "project_logger", config_path: str = "config.yaml"):
    """
    Creates and returns a logger with settings defined in config.yaml.
    Ensures consistent logging format and file handling across modules.
    """
    # Load config.yaml if available
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        log_dir = config.get('paths', {}).get('logs_dir', './logs')
        log_file = config.get('logging', {}).get('file', 'project.log')
        log_level_str = config.get('logging', {}).get('level', 'INFO')
    else:
        log_dir = "./logs"
        log_file = "project.log"
        log_level_str = "INFO"

    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_file)

    log_level = getattr(logging, log_level_str.upper(), logging.INFO)

    # Configure logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if not logger.handlers:
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # File handler
        fh = logging.FileHandler(log_path, mode='a')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
