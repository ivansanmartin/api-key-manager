from fastapi import APIRouter, Depends, status
from typing import Union
from app.services.api_key_service import ApiKeyService
from app.core.dependencies import get_api_key_manager_service
from app.models.api_key_models import ApiReferenceModel, ApiKeyModel

router = APIRouter()

# @router.post('/api-key-manager', status_code=status.HTTP_200_OK)
# async def get_api_key(api_key_service: ApiKeyService = Depends(get_api_key_manager_service)):
#     pass

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

@router.delete('/api-key-manager/{api_key_reference_id}/delete-key/{api_key_id}', status_code=status.HTTP_200_OK)
async def delet_api_key(api_key_reference_id, 
                                  api_key_id,
                                  api_key_service: ApiKeyService = Depends(get_api_key_manager_service)):
    response = api_key_service.delete_api_key(api_key_reference_id, api_key_id)
    
    return response
        
        
        
    
