import os
from azb_manager.azb_manager import AzureBlobStorageAccountManager
from tests.config import Config 

cur_dir = os.path.dirname(os.path.realpath(__file__))
if os.path.basename(cur_dir) != 'tests': 
    raise ValueError("Wrong directory - have you moved this file?") 

download_dir = os.path.join(cur_dir, 'downloads')
if not os.path.exists(download_dir): 
    os.makedirs(download_dir)

# AZURE_SA_MANAGER = AzureBlobStorageAccountManager(
#             connection_str=Config.AZURE_CONNECTION_STRING,
#             download_dir=download_dir)

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

