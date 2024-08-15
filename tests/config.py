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
        
    # Secrets 
    AZURE_STORAGE_ACCOUNT = os.environ.get("AZURE_STORAGE_ACCOUNT")
    AZURE_CONNECTION_STRING = os.environ.get('AZURE_CONNECTION_STRING')
    AZURE_CONTAINER_NAME = os.environ.get("AZURE_CONTAINER_NAME")

# Mock data for tests  
import json 
import csv 
from io import BytesIO

class TestData: 
    mock_json_dict={'mytest':'json'}
    mock_json_bin_str=json.dumps(mock_json_dict).encode('utf-8') 

    mock_csv_str="date,fruit\ntoday,apple\ntomorrow,orange" 
    mock_csv_str_bin=BytesIO(mock_csv_str.encode('utf-8'))

    connection_strings = [
        ('DefaultEndpointsProtocol=https;AccountName=mockstorageaccount1;AccountKey=abcdefghijklmnopqrstuvwx/1234567890abcdefghijklmnopqrstuvwxyz=;EndpointSuffix=core.windows.net',
            {
                "DefaultEndpointsProtocol" : "https",
                "AccountName" : "mockstorageaccount1",
                "AccountKey" : "abcdefghijklmnopqrstuvwx/1234567890abcdefghijklmnopqrstuvwxyz=",
                "EndpointSuffix" : "core.windows.net",
            }),
        
        ('DefaultEndpointsProtocol=https;AccountName=mockstorageaccount2;AccountKey=mnopqrstuvwx1234567890abcdefghijklmnopqrstuvwx/1234567890=;BlobEndpoint=https://customdomain.com;TableEndpoint=https://customdomain.com;QueueEndpoint=https://customdomain.com;FileEndpoint=https://customdomain.com',
         {
            "DefaultEndpointsProtocol" : "https",
            "AccountName" : "mockstorageaccount2",
            "AccountKey" : "mnopqrstuvwx1234567890abcdefghijklmnopqrstuvwx/1234567890=",
            "BlobEndpoint" : "https://customdomain.com",
            "TableEndpoint" : "https://customdomain.com",
            "QueueEndpoint" : "https://customdomain.com",
            "FileEndpoint" : "https://customdomain.com",

         }),
        
        ('SharedAccessSignature=sv=2023-01-01&ss=b&srt=sco&sp=rwdlacupx&se=2024-12-31T23:59:59Z&st=2024-01-01T00:00:00Z&spr=https,http&sig=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz%2F1234567890=;BlobEndpoint=https://mockstorageaccount3.blob.core.windows.net;QueueEndpoint=https://mockstorageaccount3.queue.core.windows.net;FileEndpoint=https://mockstorageaccount3.file.core.windows.net;TableEndpoint=https://mockstorageaccount3.table.core.windows.net;',
            {
                "SharedAccessSignature" : "sv=2023-01-01&ss=b&srt=sco&sp=rwdlacupx&se=2024-12-31T23:59:59Z&st=2024-01-01T00:00:00Z&spr=https,http&sig=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz%2F1234567890=",
                "BlobEndpoint" : "https://mockstorageaccount3.blob.core.windows.net",
                "QueueEndpoint" : "https://mockstorageaccount3.queue.core.windows.net",
                "FileEndpoint" : "https://mockstorageaccount3.file.core.windows.net",
                "TableEndpoint" : "https://mockstorageaccount3.table.core.windows.net",
            }        
         )]



cur_dir = os.path.dirname(os.path.realpath(__file__))
if os.path.basename(cur_dir) != 'tests': 
    raise ValueError("Wrong directory - have you moved this file?") 

DOWNLOAD_DIR = os.path.join(cur_dir, 'downloads')
