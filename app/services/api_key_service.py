from pymongo.collection import Collection
from app.models.api_key_model import ApiKeyModel
from pymongo.errors import PyMongoError

class ApiKeyService():
    def __init__(self, collection: Collection):
        self.collection = collection
        
    