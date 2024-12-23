from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError, PyMongoError

class MongoDB:
    def __init__(self, uri: str, database_name: str):
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.database = self.client[database_name]
            self.client.admin.command('ping')
            print(f'Successfully connected to {database_name}')
        except ConnectionFailure as e:
            raise RuntimeError(f'Failed to connect to MongoDB: {str(e)}')
        except ConfigurationError as e:
            raise RuntimeError(f'Configuration error in MongoDB: {str(e)}')
        except PyMongoError as e:
            raise RuntimeError(f'Unexpected MongoDB error: {str(e)}')
        
    def get_collection(self, name: str):
        try:
            if name not in self.database.list_collection_names():
                raise ValueError(f'Collection "{name}" does not exist')
            return self.database[name]
        except PyMongoError as e:
            raise RuntimeError(f'Error retrieving collection "{name}": {str(e)}')