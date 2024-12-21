from fastapi import Depends
from app.db.database import MongoDB
from app.services.api_key_service import ApiKeyService
from app.core.config import env

mongodb_credentials = env.get('mongodb')
mongodb_url = mongodb_credentials.get('url')
mongodb_port = mongodb_credentials.get('port')
mongodb_username = mongodb_credentials.get('username')
mongodb_password = mongodb_credentials.get('password')
mongodb_database = mongodb_credentials.get('database')
mongodb_collection = mongodb_credentials.get('collection')

mongodb = MongoDB(uri=f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_url}:{mongodb_port}",
                    database_name=mongodb_database)

api_key_manager_collection = mongodb.get_collection(mongodb_collection)

def get_api_key_manager_service() -> ApiKeyService:
    return ApiKeyService(api_key_manager_collection)
