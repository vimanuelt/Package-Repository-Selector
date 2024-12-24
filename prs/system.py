# prs/system.py

import subprocess
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def update_repository(source, dest, password):
    """
    Copies 'source' file to 'dest' using sudo. 
    'password' is piped into 'sudo -S' for authentication if needed.
    """
    command = f'echo "{password}" | sudo -S cp {source} {dest}'
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        logger.info(f"Command '{command}' executed successfully.")
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with error: {e}")
        logger.error(f"Command output: {e.stdout}")
        logger.error(f"Command error: {e.stderr}")
        return False

