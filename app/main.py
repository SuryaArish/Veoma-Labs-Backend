from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.routers import designing, feedback, printer_product, scanning, workshop

app = FastAPI(title="Veoma Labs API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(SQLAlchemyError)
async def db_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": str(exc)})


app.include_router(printer_product.router)
app.include_router(scanning.router)
app.include_router(designing.router)
app.include_router(feedback.router)
app.include_router(workshop.router)


@app.get("/", tags=["Health"])
async def health_check() -> dict:
    return {"status": "ok", "message": "Veoma Labs API is running"}
