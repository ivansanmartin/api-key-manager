from fastapi import APIRouter, Depends, status
from app.services.api_key_service import ApiKeyService
from app.core.dependencies import get_api_key_manager_service
from app.models.api_key_model import ApiKeyModel

router = APIRouter()

@router.post("/api-key-manager", status_code=status.HTTP_200_OK)
async def get_api_key(api_key_service: ApiKeyService = Depends(get_api_key_manager_service)):
    pass
