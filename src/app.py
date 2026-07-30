from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.config import get_settings
from src.routers import assistente, atendimentos, auth, clientes, dashboard, termo, users

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
app.include_router(atendimentos.foto_router)
app.include_router(users.router)
app.include_router(termo.router)
app.include_router(assistente.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
