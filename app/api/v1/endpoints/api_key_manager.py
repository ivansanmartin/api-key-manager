from fastapi import APIRouter, Depends, status
from app.services.api_key_service import ApiKeyService
from app.core.dependencies import get_api_key_manager_service
from app.models.api_key_models import ApiReferenceModel, ApiKeyModel, VerifyKeyModel

router = APIRouter()

@router.post('/api-key-manager', status_code=status.HTTP_201_CREATED)
async def create_api_key_reference(api_reference: ApiReferenceModel, 
                        api_key_service: ApiKeyService = Depends(get_api_key_manager_service)):
    response = api_key_service.create_api_key_reference(api_reference.model_dump())
    
    return response

@router.patch('/api-key-manager/{api_key_reference_id}', status_code=status.HTTP_200_OK)
async def update_api_key_reference(api_reference_changes: ApiReferenceModel, 
                         api_key_reference_id, 
                         api_key_service: ApiKeyService = Depends(get_api_key_manager_service)):
    response = api_key_service.update_api_key_reference(api_key_reference_id, api_reference_changes.model_dump(exclude_unset=True))
    
    return response

@router.delete('/api-key-manager/{api_key_reference_id}', status_code=status.HTTP_200_OK)
async def delete_api_key_reference(api_key_reference_id,
                                   api_key_service: ApiKeyService = Depends(get_api_key_manager_service)):
   response = api_key_service.delete_api_key_reference(api_key_reference_id)
   
   return response

@router.patch('/api-key-manager/generate-key/{api_key_reference_id}', status_code=status.HTTP_200_OK)
async def generate_api_key(api_key: ApiKeyModel, api_key_reference_id,
                           api_key_service: ApiKeyService = Depends(get_api_key_manager_service)):
    response = api_key_service.generate_api_key(api_key_reference_id, api_key)

    return response

@router.delete('/api-key-manager/{api_key_reference_id}/delete-key/{api_key_id}', status_code=status.HTTP_200_OK)
async def delete_api_key(api_key_reference_id, 
                         api_key_id,
                         api_key_service: ApiKeyService = Depends(get_api_key_manager_service)):
    response = api_key_service.delete_api_key(api_key_reference_id, api_key_id)
    
    return response

@router.post('/api-key-manager/verify-key', status_code=status.HTTP_200_OK)
async def verify_api_key(api_key: VerifyKeyModel,
                         api_key_service: ApiKeyService = Depends(get_api_key_manager_service)):
    response = api_key_service.verify_api_key(api_key)
    
    return response
    