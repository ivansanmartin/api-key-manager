from fastapi import FastAPI, Request, status
from app.api.v1.endpoints.api_key_manager import router as api_key_router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

app.include_router(api_key_router, prefix="/api/v1")
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"ok": False, "message": "error"}
    )

@app.get("/")
async def main():
    return {"ok": True, "name": "api-key-manager.", "descripcion": "API Key generator and administrator", "author": "Iván San Martín"}