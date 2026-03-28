from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.modules.playlist.playlist_controller import router as playlist_router
from app.modules.user.user_controller import router as user_router
from app.modules.auth.auth_controller import router as auth_router

app = FastAPI()

# ✅ Criar tabelas
Base.metadata.create_all(bind=engine)

# 🔹 Configuração CORS - colocar antes de incluir routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # endereço do seu front-end React
    allow_credentials=True,
    allow_methods=["*"],  # permite GET, POST, PUT, DELETE...
    allow_headers=["*"],  # permite enviar Authorization, Content-Type, etc.
)

# ✅ Incluir routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(playlist_router)

@app.get("/")
def root():
    return {"message": "Marketplace API running"}