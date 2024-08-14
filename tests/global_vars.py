from .config import Config 
import os
from azb_client.AzureBlobStorageClient import AzureBlobStorageAccountManager

cur_dir = os.path.dirname(os.path.realpath(__file__))
if os.path.basename(cur_dir) != 'test': 
    raise ValueError("Wrong directory - have you moved this file?") 
download_dir = os.path.join(cur_dir, 'temp')
if not os.path.exists(download_dir): 
    os.makedirs(download_dir)

AZURE_SA_MANAGER = AzureBlobStorageAccountManager(
            connection_str=Config.secrets.AZURE_CONNECTION_STRING,
            download_dir=download_dir)
ex_container_client = getattr(AZURE_SA_MANAGER, Config.secrets.CONTAINER_1)

# Mock data for tests  
import json 
import csv 
import BytesIO

mock_json_dict={'mytest':'json'}
mock_json_bin_str=json.dumps(mock_json_dict).encode('utf-8') 

mock_csv_str="date,fruit\ntoday,apple\ntomorrow,orange" 
mock_csv_str_bin=BytesIO(mock_csv_str.encode('utf-8'))