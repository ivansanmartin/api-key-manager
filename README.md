# API Key Manager Service Documentation

## Overview
The API Key Manager Service provides a complete solution for managing API keys, including creation, verification, and management of API references. It uses MongoDB for persistent storage and Redis for caching verification results.

## Base URL
```
/api-key-manager
```

## Authentication
This service manages API key authentication but does not specify authentication requirements for the management endpoints themselves (NOT YET).

## Endpoints

### 1. Create API Key Reference
Creates a new API reference entry.

**Endpoint:** `POST /api-key-manager`  
**Status Code:** 201 Created

**Request Body:**
```json
{
  "name": "string",
  "description": "string",
  "api_keys": []
}
```

**Response:**
```json
{
  "ok": true,
  "message": "API reference created successfully.",
  "data": {
    "_id": "string",
    "name": "string",
    "description": "string",
    "api_keys": []
  }
}
```

### 2. Update API Key Reference
Updates an existing API reference entry.

**Endpoint:** `PATCH /api-key-manager/{api_key_reference_id}`  
**Status Code:** 200 OK

**Path Parameters:**
- `api_key_reference_id`: String (MongoDB ObjectId)

**Request Body:**
```json
{
  "name": "string",
  "description": "string"
}
```

**Response:**
```json
{
  "ok": true,
  "message": "API reference updated successfully."
}
```

### 3. Delete API Key Reference
Deletes an API reference and all associated API keys.

**Endpoint:** `DELETE /api-key-manager/{api_key_reference_id}`  
**Status Code:** 200 OK

**Path Parameters:**
- `api_key_reference_id`: String (MongoDB ObjectId)

**Response:**
```json
{
  "ok": true,
  "message": "API reference deleted successfully"
}
```

### 4. Generate API Key
Generates a new API key for an existing API reference.

**Endpoint:** `PATCH /api-key-manager/generate-key/{api_key_reference_id}`  
**Status Code:** 200 OK

**Path Parameters:**
- `api_key_reference_id`: String (MongoDB ObjectId)

**Request Body:**
```json
{
  "id": "string",
  "expiration_date": "string (ISO date)"
}
```

**Response:**
```json
{
  "ok": true,
  "api_reference_id": "string",
  "message": "API key generated successfully in api reference.",
  "data_key": {
    "id": "string",
    "api_key": "string",
    "expiration_date": "string"
  }
}
```

### 5. Delete API Key
Removes a specific API key from an API reference.

**Endpoint:** `DELETE /api-key-manager/{api_key_reference_id}/delete-key/{api_key_id}`  
**Status Code:** 200 OK

**Path Parameters:**
- `api_key_reference_id`: String (MongoDB ObjectId)
- `api_key_id`: String

**Response:**
```json
{
  "ok": true,
  "message": "API key of reference deleted successfully"
}
```

### 6. Verify API Key
Verifies the validity of an API key.

**Endpoint:** `POST /api-key-manager/verify-key`  
**Status Code:** 200 OK

**Request Body:**
```json
{
  "api_reference_id": "string",
  "api_key_id": "string",
  "api_key": "string"
}
```

**Response:**
```json
{
  "ok": true,
  "message": "API Key is correct and verified.",
  "api_reference": {
    "name": "string",
    "description": "string"
  }
}
```

## Error Responses

### Not Found (404)
```json
{
  "ok": false,
  "message": "API reference not found."
}
```
or
```json
{
  "ok": false,
  "message": "API key not found in api reference."
}
```
or
```json
{
  "ok": false,
  "message": "API Key is expire or doesnt exist."
}
```

### MongoDB Error
```json
{
  "ok": false,
  "error": "MongoDB error message"
}
```

## Technical Details

### Caching
- API key verification results are cached in Redis for 1 hour (3600 seconds)
- Cache key format: `api_key_id:{api_key_id}`

### Security Features
- API keys are hashed using bcrypt before storage
- Generated API keys follow the format: `key_{random_string}`
- API key length: 32 characters (excluding prefix)

### Dependencies
- MongoDB for persistent storage
- Redis for caching
- FastAPI framework
- PyMongo for MongoDB operations
- bcrypt for key hashing
- secrets for secure key generation

## Models

### ApiReferenceModel
```python
{
    "name": str,
    "description": str,
    "api_keys": List[ApiKeyModel]
}
```

### ApiKeyModel
```python
{
    "id": str,
    "key": str,  # Hashed value
    "expiration_date": datetime
}
```

### VerifyKeyModel
```python
{
    "api_reference_id": str,
    "api_key_id": str,
    "api_key": str
}
```