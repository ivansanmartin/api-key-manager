from fastapi import Depends
from app.db.database import MongoDB, Redis
from app.services.api_key_service import ApiKeyService
from app.core.config import env

mongodb_credentials = env.get('mongodb')

[mongodb_url, mongodb_port,
 mongodb_username, mongodb_password, 
 mongodb_database, mongodb_collection] = mongodb_credentials.get('url'), mongodb_credentials.get('port'), mongodb_credentials.get('username'), mongodb_credentials.get('password'), mongodb_credentials.get('database'), mongodb_credentials.get('collection')

redis_credentials = env.get('redis')

[redis_username, redis_password, redis_host, redis_port] = redis_credentials.get('username'), redis_credentials.get('password'), redis_credentials.get('host'), redis_credentials.get('port')

mongodb = MongoDB(uri=f'mongodb://{mongodb_username}:{mongodb_password}@{mongodb_url}:{mongodb_port}',
                    database_name=mongodb_database)

redis_instance = Redis(redis_url=f'redis://{redis_username}:{redis_password}@{redis_host}:{redis_port}/0')

redis = redis_instance.get_redis()

api_key_manager_collection = mongodb.get_collection(mongodb_collection)

def get_api_key_manager_service() -> ApiKeyService:
    return ApiKeyService(api_key_manager_collection, redis)
