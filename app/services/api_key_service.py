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
            api_reference['_id'] = str(api_reference['_id'])
            api_reference = {'_id': api_reference['_id'], **api_reference}

            return {'ok': True, 'message': 'API reference created successfully.', 'data': api_reference}
        except PyMongoError as e:
            return {'ok': False, 'error': e}
    
    def update_api_key_reference(self, api_key_reference_id: str, api_reference_changes: ApiReferenceModel) -> dict:
        try:
            response = self.collection.update_one({'_id': ObjectId(api_key_reference_id)}, {'$set': api_reference_changes})
            
            if response.matched_count == 0:
                return {'ok': False, 'message': 'API reference not found.'}

            return {'ok': True, 'message': 'API reference updated successfully.'}
            
        except PyMongoError as e:
            return {'ok': False, 'error': e}
        
    def delete_api_key_reference(self, api_key_reference_id: str) -> dict:
        try:
            response = self.collection.delete_one({'_id': ObjectId(api_key_reference_id)})
            
            if response.deleted_count == 0:
                return {'ok': False, 'message': 'API reference not found.'}

            return {'ok': True, 'message': 'API reference deleted successfully'}
        except PyMongoError as e:
            return {'ok': False, 'error': e}
            
        
    def delete_api_key(self, api_key_reference_id: str, api_key_id: str) -> dict:
        try:

            if (not self._exist_api_reference(api_key_reference_id)):
                return {'ok': False, 'message': 'API reference not found.'}
            
            if (not self._exist_api_key(api_key_reference_id, api_key_id)):
                return {'ok': False, 'message': 'API key not found in api reference.'}

            self.collection.update_one(
                    {'_id': ObjectId(api_key_reference_id), 'api_keys.id': api_key_id},
                    {
                        '$pull': {
                            'api_keys': { 'id': api_key_id }
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
                    'id': api_key['id'],
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
    
    def _exist_api_reference(self, api_key_reference_id):
        try:
            response = self.collection.find_one({'_id': ObjectId(api_key_reference_id)})
            if response:
                return True
            else:
                return False
            
        except PyMongoError as e:
            return {'ok': False, 'error': e}



    def _exist_api_key(self, api_key_reference_id, api_key_id):
        try:
            response = self.collection.find_one(
                {
                    '_id': ObjectId(api_key_reference_id),
                    'api_keys': {
                        '$elemMatch': {'id': api_key_id}
                    }
                }
            )

            if response:
                return True
            else:
                return False

        except PyMongoError as e:
            return {'ok': False, 'error': e}