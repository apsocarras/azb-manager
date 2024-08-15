## Test that Storage Account Manager can be initialized and run same functions as its constituent container managers
import pytest 
import os 
from .config import get_logger, set_logging_level,Config, TestData, DOWNLOAD_DIR
import logging 


logger = get_logger()
set_logging_level(logging.DEBUG)

from azb_manager.azb_manager import AzureBlobStorageAccountManager

@pytest.mark.parametrize('data,blob_name,file_name', [

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
def test_upload_blob(data, blob_name, file_name): 

    
    if file_name: 
        _file_name=os.path.join('uploads', file_name)
        if not os.path.exists(_file_name): 
            raise FileNotFoundError(f'{_file_name} does not exist (error in test configuration)')
    else: 
        _file_name = None 

    azb_storage_account = AzureBlobStorageAccountManager(storage_account_name=Config.AZURE_STORAGE_ACCOUNT,
                                   connection_str=Config.AZURE_CONNECTION_STRING,
                                   download_dir=DOWNLOAD_DIR)
    
    azb_storage_account.upload_blob(data=data, 
                                    blob_name=blob_name, 
                                    file_name=_file_name, 
                                    container_name=Config.AZURE_CONTAINER_NAME,
                                    overwrite=True, 
                                    encode_json=True)







