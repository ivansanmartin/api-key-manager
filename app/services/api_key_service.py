from pymongo.collection import Collection
from app.models.api_key_models import ApiReferenceModel
from pymongo.errors import PyMongoError

class ApiKeyService():
    def __init__(self, collection: Collection):
        self.collection = collection
        
    def create_api_key(self, api_reference: ApiReferenceModel):
        try:
            self.collection.insert_one(api_reference)
            return {"ok": True, "message": "API reference created successfully."}
        except PyMongoError as e:
            return {"ok": False, "error": e}
    
    def update_api_key(self, api_reference: ApiReferenceModel):
        pass
        
        
    