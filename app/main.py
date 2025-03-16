from fastapi import FastAPI, Request, status
from app.api.v1.endpoints.api_key_manager import router as api_key_router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "https://ivsm.link",
    "http://url-shortener-service.ivansanmartin.svc.cluster.local"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_key_router, prefix="/api/v1")

@app.get("/")
async def main():
    return {"ok": True, "name": "api-key-manager.", "descripcion": "API Key generator and administrator", "author": "Iván San Martín"}