from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.modules.playlist.playlist_controller import router as playlist_router
from app.modules.user.user_controller import router as user_router
from app.modules.auth.auth_controller import router as auth_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

#  Configuração CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],  # permite GET, POST, PUT, DELETE
    allow_headers=["*"],  # permite enviar Authorization, Content-Type, etc.
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(playlist_router)

@app.get("/")
def root():
    return {"message": "Bestfy API running"}