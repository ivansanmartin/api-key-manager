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
}
