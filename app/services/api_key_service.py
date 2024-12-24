from pymongo.collection import Collection
from app.models.api_key_models import ApiReferenceModel, ApiKeyModel
from pymongo.errors import PyMongoError
from typing import Union
from bson import ObjectId
import secrets
import bcrypt

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

            # TODO:

            # Validate if exist api reference and api key in api reference

            response = self.collection.update_one(
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
        
    def generate_api_key(self, api_key_reference_id, api_key: ApiKeyModel):
        try:
            api_key_generate_hashed, api_key_generate = self._generate_secret_api_key('key')
            api_key = api_key.model_copy(update={'key': api_key_generate_hashed}).model_dump()
            response = self.collection.update_one(
                {'_id': ObjectId(api_key_reference_id)},
                {'$addToSet': {
                    'api_keys': api_key
                }}
            )

            if response.matched_count == 0:
                return {'ok': False, 'message': 'API reference not found.'}


            return {
                'ok': True, 
                'message': 'API key generated succesfully in api reference',
                'data': {
                    'api_key': api_key_generate,
                    'expiration_date': api_key['expiration_date']
                }
            }
        except PyMongoError as e:
            return {'ok': False, 'error': e}


    def _generate_secret_api_key(self, prefix: str, length=32) -> str:
        return self._hash_api_key(f"{prefix}_{secrets.token_urlsafe(length)}"), f"{prefix}_{secrets.token_urlsafe(length)}"
    
    def _hash_api_key(self, api_key: str):
        salt = bcrypt.gensalt()
        hashed_key = bcrypt.hashpw(api_key.encode(), salt)
        
        return hashed_key.decode()
    
    def _verify_api_key(self, api_key: str, hashed_key: str) -> bool:
        return bcrypt.checkpw(api_key.encode(), hashed_key.encode())

            
            
            
        
        
        
    