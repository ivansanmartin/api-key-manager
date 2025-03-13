from fastapi import FastAPI
from app.api.v1.endpoints.api_key_manager import router as api_key_router

app = FastAPI()

app.include_router(api_key_router, prefix="/api/v1")

@app.get("/")
async def main():
    return {"ok": True, "name": "api-key-manager.", "descripcion": "API Key generator and administrator", "author": "Iván San Martín"}