from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.config import get_settings
from src.routers import atendimentos, auth, clientes, dashboard

settings = get_settings()

app = FastAPI(title="Lava Rápido API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(clientes.router)
app.include_router(atendimentos.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
