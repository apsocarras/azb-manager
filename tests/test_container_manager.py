import pytest 
import json 
import os
# import csv 
# from .global_vars import *
import logging 
from .config import get_logger, set_logging_level,Config, TestData, DOWNLOAD_DIR
from azb_manager.azb_manager import AzureBlobContainerManager

logger = get_logger()
set_logging_level(logging.DEBUG)

@pytest.mark.parametrize("data,blob_name,file_name", 
    [
     # Uploading Python Objects 
     (TestData.mock_json_dict, 'mock_json_dict.json', None, ),
     (TestData.mock_json_bin_str, 'mock_json_bin_str.json', None, ), 
     (TestData.mock_csv_str, 'mock_csv_str.json', None, ), 
     (TestData.mock_csv_str_bin, 'mock_csv_str_bin.json', None),
    
     # From File Paths
     (None, None, 'mock.json', ),
     (None, 'mock_json_custom_name.csv', 'mock.json',),
     (None, None, 'mock.csv',), 
     (None, 'mock_csv_custom_name.csv', 'mock.csv',), 
       
     ])
def test_upload_blob(data,blob_name,file_name) -> None:
    """Test blob upload. Successful if has_blob obtained"""
    
    if file_name: 
        _file_name=os.path.join('uploads', file_name)
        if not os.path.exists(_file_name): 
            raise FileNotFoundError(f'{_file_name} does not exist (error in test configuration)')
    else: 
        _file_name = None 

    azb_container = AzureBlobContainerManager(connection_str=Config.AZURE_CONNECTION_STRING,
                                              container_name=Config.AZURE_CONTAINER_NAME, 
                                              download_dir=DOWNLOAD_DIR)

    azb_container.upload_blob(data=data,
                            blob_name=blob_name, 
                            file_name=_file_name, 
                            overwrite=True, 
                            encode_json=True)
    
    # Check if blob is in container
    if blob_name is not None:
        hasblob=azb_container.has_blob(blob_name)
        logger.debug(f"{azb_container.container_name}: has_blob('{blob_name}')={hasblob}")
    elif file_name is not None: 
        hasblob=azb_container.has_blob(file_name)
        logger.debug(f"{azb_container.container_name}: has_blob('{file_name}')={hasblob}")


@pytest.mark.parametrize('blob_name',[

    TestData.mock_json_dict,
    TestData.mock_json_bin_str,
    TestData.mock_csv_str,
    TestData.mock_csv_str_bin,

])
def test_download_blob(blob_name):
    azb_container = AzureBlobContainerManager(connection_str=Config.AZURE_CONNECTION_STRING,
                                    container_name=Config.AZURE_CONTAINER_NAME, 
                                    download_dir=DOWNLOAD_DIR)
    
    for b in azb_container.list_blobs(name_only=True): 
        print(b)
        b_bytes = azb_container.download_blob_bytes(b)
        b_file = azb_container.download_blob_file(b)    
