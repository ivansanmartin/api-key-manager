from pymongo.collection import Collection
from redis import Redis
from app.models.api_key_models import ApiReferenceModel, ApiKeyModel, VerifyKeyModel
from pymongo.errors import PyMongoError
from fastapi.responses import JSONResponse
from fastapi import status
from bson import ObjectId
import secrets
import bcrypt
from bson import json_util
import json

class ApiKeyService():
    def __init__(self, collection: Collection, redis: Redis):
        self.collection = collection
        self.redis = redis
        
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
                return JSONResponse(
                    content={'ok': False, 'message': 'API reference not found.'},
                    status_code=status.HTTP_404_NOT_FOUND
                )

            return {'ok': True, 'message': 'API reference updated successfully.'}
            
        except PyMongoError as e:
            return {'ok': False, 'error': e}
        
    def delete_api_key_reference(self, api_key_reference_id: str) -> dict:
        try:
            response = self.collection.delete_one({'_id': ObjectId(api_key_reference_id)})
            
            if response.deleted_count == 0:
                return JSONResponse(
                    content={'ok': False, 'message': 'API reference not found.'},
                    status_code=status.HTTP_404_NOT_FOUND
                )

            return {'ok': True, 'message': 'API reference deleted successfully'}
        except PyMongoError as e:
            return {'ok': False, 'error': e}
            
        
    def delete_api_key(self, api_key_reference_id: str, api_key_id: str) -> dict:
        try:

            if (not self._exist_api_reference(api_key_reference_id)):
                return JSONResponse(
                    content={'ok': False, 'message': 'API reference not found.'},
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            if (not self._exist_api_key(api_key_reference_id, api_key_id)):
                return JSONResponse(
                    content={'ok': False, 'message': 'API key not found in api reference.'},
                    status_code=status.HTTP_404_NOT_FOUND
                )

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
                return JSONResponse(
                    content={'ok': False, 'message': 'API reference not found.'},
                    status_code=status.HTTP_404_NOT_FOUND
                )
                
            return {
                'ok': True, 
                'api_reference_id': api_key_reference_id,
                'message': 'API key generated succesfully in api reference.',
                'data_key': {
                    'id': api_key['id'],
                    'api_key': api_key_generate,
                    'expiration_date': api_key['expiration_date']
                }
            }
        
        except PyMongoError as e:
            return {'ok': False, 'error': e}
        
    def verify_api_key(self, api_key: VerifyKeyModel):
        try:
                
            api_data_request = api_key.model_dump()
            api_key_id = api_data_request.get('api_key_id')
            
            api_key_caching = self.redis.json().get(f'api_key_id:{api_key_id}', '$')
            if api_key_caching:
                return JSONResponse(
                    content=api_key_caching
                )
                
            [api_reference_id, api_key_id, key] = api_data_request.get('api_reference_id'), api_data_request.get('api_key_id'), api_data_request.get('api_key')
            api_reference = self._get_api_key(api_reference_id, api_key_id, key)
            if not api_reference:
                return JSONResponse(
                    content={'ok': False, 'message': 'API Key is expire or doesnt exist.'},
                    status_code=status.HTTP_404_NOT_FOUND
                )
                
            content_response = {
                    'ok': True,
                    'message': 'API Key is correct and verified.',
                    'api_reference': {
                        'name': api_reference.get('name'),
                        'description': api_reference.get('description')
                    }
                }                
                
            self.redis.json().set(f'api_key_id:{api_key_id}', '$', content_response)
            self.redis.expire(f'api_key_id:{api_key_id}', 3600)

            return JSONResponse(
                content=content_response
            )
            
        except PyMongoError as e:
            return {'ok': False, 'error': e}

    def _generate_secret_api_key(self, prefix: str, length=32) -> str:
        api_key_raw = f"{prefix}_{secrets.token_urlsafe(length)}"
        return self._hash_api_key(api_key_raw), api_key_raw
    
    def _hash_api_key(self, api_key: str):
        salt = bcrypt.gensalt()
        hashed_key = bcrypt.hashpw(api_key.encode(), salt)
        
        return hashed_key.decode()
    
    def _get_api_key(self, api_reference_id: str, api_key_id: str, api_key: str):
        response = self.collection.find_one(
            {'_id': ObjectId(api_reference_id), 'api_keys.id': api_key_id},
            {
                'api_keys': {'$elemMatch': {'id': api_key_id}},
                'name': 1,
                'description': 1
            }
        )
        
        api_key_encrypted = response.get('api_keys')[0].get('key')
        
        is_valid = self._verify_api_key(api_key, api_key_encrypted)
        
        if response and is_valid:
            return response
        else:
            return False
        
        
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