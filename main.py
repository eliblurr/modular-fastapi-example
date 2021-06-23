from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine

from routers.auth_router import models
from routers.item_router import models

from fastapi.security import OAuth2PasswordBearer

api = FastAPI(docs_url="/api/docs")

origins = ["http://localhost/*","http://localhost:8080","http://localhost:3000"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/authenticate")

from routers.auth_router import main as auth
from routers.item_router import main as items

api.include_router(auth.router,prefix="/api/user",tags=["user"])
api.include_router(items.router,prefix="/api/item",tags=["item"])

@api.get("/")
def welcome():
    return "Welcome to Neutrons link"