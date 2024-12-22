from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ApiKeyModel(BaseModel):
    name: str = Field(title='Key name', examples=['url-shortener'],
                        min_length=5, max_length=100)
    key: str = Field(title='Encrypt API Key', min_length=10, max_length=30)
    expiration_date: datetime = Field(description="Expiration date for the shortened URL")


class ApiReferenceModel(BaseModel):
    name: str = Field(title='API Rest/Service Name', examples=['url-shortener', 'binary-decimal-api'],
                            min_length=5, max_length=100)
    description: Optional[str] = Field(title='API Rest/Service short description', examples=['url-shortener is a simple api for create shorts urls'],
                             min_length=5, max_length=400)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Date and time of the API reference")
    updated_at: Optional[datetime] = Field(None, description="Date and time of the last update")
    data: Optional[List[ApiKeyModel]] = Field(default=None, title='List of Key info for api')
