import logging 
import os 
from dotenv import load_dotenv

load_dotenv()

## Logging 
logger = logging.getLogger(__name__)

if not logger.hasHandlers(): 
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

def set_logging_level(level):
    """
    Sets the logging level for the (global?) logger.

    :param level: Logging level (e.g., logging.DEBUG, logging.INFO)
    """
    logger.setLevel(level)

def get_logger(name=__name__):
    f"""
    Returns a logger with the specified name.

    (Propagates the logger settings from the logger instance defined in the module {name} where this function was defined )
    """
    return logging.getLogger(name)

class Config:

    class Secrets:

        def __init__(self, *secrets) -> None:
            """
            Load a list of secrets from environmental file (default) or local.settings.json  
            """
            
            for s in secrets:
                env_val = os.environ.get(s)
                if not env_val: 
                    raise print(f'{s} value not set in .env file.')
                setattr(self, s, env_val)
                    
    secrets = Secrets("AZURE_STORAGE_ACCOUNT",
                      'AZURE_CONNECTION_STRING', 
                      "CONTAINER_1"
                      "CONTAINER_2"
                      "CONTAINER_3") 
    
    

