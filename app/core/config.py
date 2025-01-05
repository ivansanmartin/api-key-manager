from dotenv import load_dotenv
import os

load_dotenv()

env = {
    "mongodb": {
        "url": os.getenv('MONGODB_URL'),
        "port": os.getenv('MONGODB_PORT'),
        "username": os.getenv('MONGODB_USERNAME'),
        "password": os.getenv('MONGODB_PASSWORD'),  
        "database": os.getenv('MONGODB_DATABASE'),
        "collection": os.getenv('MONGODB_COLLECTION'),
    },
    "redis": {
        'host': os.getenv('REDIS_HOST'),
        'port': os.getenv('REDIS_PORT'),
        'username': os.getenv('REDIS_USERNAME'),
        'password': os.getenv('REDIS_PASSWORD'),
    }
}
