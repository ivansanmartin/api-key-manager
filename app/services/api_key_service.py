from pymongo.collection import Collection
from app.models.api_key_models import ApiReferenceModel, ApiKeyModel
from pymongo.errors import PyMongoError
from typing import Union
from bson import ObjectId

class ApiKeyService():
    def __init__(self, collection: Collection):
        self.collection = collection
        
    def create_api_key_reference(self, api_reference: ApiReferenceModel) -> dict:
        try:
            self.collection.insert_one(api_reference)
            return {'ok': True, 'message': 'API reference created successfully.'}
        except PyMongoError as e:
            return {'ok': False, 'error': e}
    
    def update_api_key_reference(self, api_key_reference_id: str, api_reference_changes: ApiReferenceModel) -> dict:
        try:
            self.collection.update_one({'_id': ObjectId(api_key_reference_id)}, {'$set': api_reference_changes})
            
            return {'ok': True, 'message': 'API reference updated successfully.'}
            
        except PyMongoError as e:
            return {'ok': False, 'error': e}
        
    def delete_api_key_reference(self, api_key_reference_id: str) -> dict:
        try:
            self.collection.delete_one({'_id': ObjectId(api_key_reference_id)})
            
            return {'ok': True, 'message': 'API reference deleted successfully'}
        except PyMongoError as e:
            return {'ok': False, 'error': e}
            
        
    def delete_api_key(self, api_key_reference_id: str, api_key_id: str) -> dict:
        try:
            self.collection.update_one(
                    {'_id': ObjectId(api_key_reference_id), 'data.id': api_key_id},
                    {
                        '$pull': {
                            'data': { 'id': api_key_id }
                        }
                    }
                )
            
            return {'ok': True, 'message': 'API key of reference deleted successfully'}
        except PyMongoError as e:
            return {'ok': False, 'error': e}
            
            
            
        
        
        
    