from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas, BlobContainerClient, BlobContentInfo, BlobClient
import os
import datetime as dt 
from typing_extensions import TypedDict
import json 
from io import BytesIO
from typing import Optional 

class AzureBlobContainerManager: 
    def __init__(self, connection_str:str, container_name:str, download_dir:Optional[str]="."): 
        """Wrapper for common use cases when working with a designated storage account in Azure. 

        Args: 
            connection_str (str): Connection string to an Azure storage account. 
            container (str): Name of a containers in the storage account. 
            download_dir (Optional[str]): Optional default directory to download files to. 
        """
        self.container_client = BlobContainerClient.from_connection_string(connection_str, container_name)
        self.container_name = container_name
        self.download_dir = download_dir 

    def list_blobs(self, include_tags=False) -> list: 
        """Wrapper to list blobs in the container (Default to just blob names)"""

        blob_list = self.container_client.list_blobs()
        if include_tags:
            return [{'name':{blob.name}, "tags":blob.tags} for blob in blob_list] 
        else: 
            return [{'name':{blob.name}} for blob in blob_list] 
        
    def get_blob_url(self, file_name:str, include_sas=False, expiry_hours=1) -> str:
        """Get the url of a blob in the container""" 

        blob_base = os.path.basename(file_name)
        blob_client = self.container_client.get_blob_client(blob=blob_base)
        
        url = blob_client.url 
        
        # Generate SAS token (read only)
        if include_sas: 
            expiry_time = dt.datetime.now() + dt.timedelta(hours=expiry_hours)  # Adjust the expiration time as needed
            permissions = BlobSasPermissions(read=True)  # Adjust permissions as needed

            sas_token = generate_blob_sas(
            account_name=blob_client.account_name,
            container_name=self.container_name,
            blob_name=blob_base,
            account_key=blob_client.credential.account_key,
            permission=permissions,
            expiry=expiry_time,
            start=dt.datetime.now(), 
            protocol='https'
            )

            url += f"?{sas_token}"

            print(blob_client.account_name)

        return url

    def has_blob(self, file_name:str) -> bool: 
        """Check if the container has a blob of the given name"""

        return os.path.basename(file_name) in self.list_blobs(name_only=True) 
    
    def download_blob(self, blob_name:str, download_path=None): 
        """Download a blob from the container to local storage."""
            
        blob_client = self.container_client.get_blob_client(blob_name)

        if download_path is None:
            download_path = os.path.join(self.download_dir, os.path.basename(blob_name)) 
        
        with open(download_path, "wb") as file:
            download_bytes = blob_client.download_blob().readall()
            file.write(download_bytes)

        return 
    
    def download_bytes(self, blob_name:str) -> BytesIO: 
        """Download a blob from the container directly to a BytesIO Stream"""
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_data = BytesIO()
        blob_client.download_blob().download_to_stream(blob_data)
        blob_data.seek(0)
        return blob_data

    def upload_blob(self, data=None, file_name=None,  blob_name=None, overwrite=False, encode_json=False) -> BlobClient:
        """
        Upload a blob to blob storage in Azure
        
        Args: 
            
            data (Union[bytes, str, Iterable[AnyStr], IO[bytes]]): Data to upload 
            file_name (str): Path to a file to upload
            blob_name (str): Name of blob to create/update (if file_name, default is basename of file_name)
            overwrite (bool): Whether to overwrite a blob of the same name in the container if it already exists.   
            encode_json (bool): Whether to try to encode data to binary JSON data before uploading  

        Returns: 

        bool (BlobClient): BlobClient object for the uploaded blob.

        """

        ## Check parameters 
        # Required parameters provided 
        if (data and file_name) or (not data and not file_name): 
            raise ValueError(f"Must provide exactly one: file path or binary data.")
        if (data and not blob_name):
            raise ValueError(f'Must provide blob_name if uploading binary data.')
        # Valid parameter names 
        for x in (blob_name, file_name): 
            if x and os.path.splitext(x)[1] == '': 
                raise ValueError(f'Must include file extension in name {x}') 
               
        ## Upload blobs 
        if file_name:    
            if blob_name is None:
                blob_name = os.path.basename(file_name)
            blob_client = self.container_client.get_blob_client(blob_name)
            # Upload the file
            with open(file_name, "rb") as file:
                response = blob_client.upload_blob(file, overwrite=overwrite)
            print(f"Blob {blob_name} uploaded successfully.")

        elif data:             
            response = blob_client = self.container_client.get_blob_client(blob_name)
            # Check that provided data is valid 
            valid_types = (bytes, str, BytesIO)
            if not any(isinstance(data, t) for t in valid_types): 
                if not encode_json: 
                    raise TypeError(f"Parameter 'data' must be one of {', '.join((str(t) for t in valid_types))}")
                else: 
                    print(f"Encoding 'data' to binary JSON before uploading")
                    bin_data = self._encode_json(data)  
                    response = blob_client.upload_blob(bin_data, overwrite=overwrite)
            else: 
                response = blob_client.upload_blob(data, overwrite=overwrite)

        return response 

class AzureBlobStorageAccountManager:
    def __init__(self, 
                 connection_str:str, 
                 containers: Optional[list] = None, 
                 download_dir: Optional[str] = "."):
        """Wrapper for common use cases when working with a designated storage account in Azure via connection string. 
        
        Args: 
            connection_str (str): Connection string to an Azure storage account. 
            containers (Optional[list]): Names of containers in the storage account to use. 
            download_dir (Optional[str]): Optional default directory to download files to. 
        """

        self.blob_service_client = BlobServiceClient.from_connection_string(connection_str)
        self._set_containers(containers)

        # The default directory to which to download a blob.
        self.download_dir = download_dir

        # Parse the connection string for the storage account name 
        conn_dict = AzureBlobStorageAccountManager._parse_conn_string(connection_str) 
        self.storage_account = conn_dict['AccountName']


    def list_containers(self, include_metadata=False) -> list: 
        """List containers in the storage account along with optional metadata
        https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-containers-list-python
        """
        container_list = self.blob_service_client.list_containers
        
        if include_metadata:
            return [{'name':c['name'], 'metadata':c['metadata']} for c in container_list] 
        else: 
            return [c['name'] for c in container_list] 
        
    @classmethod
    def _encode_json(cls, data):
        """Internal wrapper to encode passed data objects to binary JSON prior to uploading.""" 
        try: 
            json_str = json.dumps(data)
            json_bin = json_str.encode('utf-8')
            return json_bin
        except Exception as e:  
            ## TO-DO: Handle individual error types 
            raise Exception(f"Failed to encode {data} to binary JSON ({str(e)})")
    @classmethod
    def _parse_conn_string(cls, conn_str:str) -> dict:
        """Extract the storage account name from a connection string"""

        expected_schema={ 
            'DefaultEndpointsProtocol': str,
            'AccountName': str,
            'AccountKey': str,
            'EndpointSuffix': str
        }

        conn_dict={}
        for key_value in conn_str.split(";"): 
            key, value = key_value.split('=')
            conn_dict[key] = value 

        if any(k not in expected_schema or not isinstance(k, expected_schema[k])
               for k in conn_dict): 
            print(f'Failed to parse connection string to expected JSON schema: \n{conn_str}\n(parsed: {conn_dict})')
            raise ValueError('Failed to parse connection string to expected JSON schema')

        return conn_dict
    
    def _set_container_clients(self, containers:Optional[list]) -> None: 
        """(Internal Helper) Get and set container clients based on container name"""
        
        container_list = containers if containers else \
            self.list_containers(include_metadata=False)

        for container_name in container_list:
            
            # Initialize Container Manager  
            container_manager = AzureBlobContainerManager(
                                connection_str=self.connection_str,
                                container_name=container_name, 
                                download_dir=self.download_dir)
            # Set as attribute 
            setattr(self, container_name, container_manager)

        return
    
    def upload_blob(self, container_name, **kwargs) -> None: 
        """Wrapper for AzureBlobContainerManager.upload_blob(). Used in tests not to expose container name."""
        try:
            container_manager = getattr(self, container_name)
            container_manager.upload_blob(**kwargs)
        except AttributeError: 
            raise AttributeError(f"Container '{container_name}' not set in attributes.")
        
    