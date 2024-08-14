import pytest 
import json 
import csv 
from .global_vars import *
import logging 
from .config import get_logger, set_logging_level
from azure.storage.blob import BlobClient

logger = get_logger()
set_logging_level(logging.DEBUG)

@pytest.mark.parameterize("data,blob_name,file_name", 
    [
     # Uploading Python Objects 
     (mock_json_dict, 'mock_json_dict', None, ),
     (mock_json_bin_str, 'mock_json_bin_str', None, ), 
     (mock_csv_str, 'mock_csv_str', None, ), 
     (mock_csv_str_bin, 'mock_csv_str_bin', None),
    
     # From File Paths
     (None, None, 'mock.json', ),
     (None, 'mock_json_custom_name', 'mock.json',),
     (None, None, 'mock.csv',), 
     (None, 'mock_csv_custom_name', 'mock.csv',), 
       
     ])
def test_upload_blob(data, blob_name,file_name) -> None:
    """Test blob upload. Successful if has_blob obtained"""
    
    if file_name: 
        _file_name=os.path.join('uploads',file_name)
        if not os.path.exists(_file_name): 
            raise FileNotFoundError(f'{_file_name} does not exist (error in test configuration)')
    else: 
        _file_name = None 

    ex_container_client.upload_blob(data=data,
                                    file_name=_file_name, 
                                    blob_name=blob_name, 
                                    overwrite=True, 
                                    encode_json=True)
    
    # Check if blob is in container
    hasblob=ex_container_client.has_blob(blob_name)
    logger.debug(f"{ex_container_client.container_name}: has_blob('{blob_name}')={hasblob}")
    

# def test_download_bytes():

# def test_download_blob(): 

