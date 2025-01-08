from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid


class ApiKeyModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), title="Unique Key ID")
    key: str = Field(default=None, title='Encrypt API Key', min_length=10, max_length=50)
    expiration_date: datetime = Field(default=None, description='Expiration date for the shortened URL')

class ApiReferenceModel(BaseModel):
    name: str = Field(title='API Rest/Service Name', examples=['url-shortener', 'binary-decimal-api'],
                            min_length=5, max_length=100)
    description: Optional[str] = Field(default=None, title='API Rest/Service short description', examples=['url-shortener is a simple api for create shorts urls'],
                             min_length=5, max_length=400)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description='Date and time of the API reference')
    updated_at: Optional[datetime] = Field(default=None, description='Date and time of the last update')
    api_keys: Optional[List[ApiKeyModel]] = Field(default=[], title='List of Key info for api')

class VerifyKeyModel(BaseModel):
    api_reference_id: str = Field(default_factory=lambda: str(uuid.uuid4()), title="Unique Key ID of API reference")
    api_key_id: str = Field(default=None, title='Encrypt API Key', min_length=10, max_length=50)
    api_key: str = Field(default=None, title='API Key', min_length=10, max_length=50)