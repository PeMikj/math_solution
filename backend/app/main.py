from dotenv import load_dotenv
load_dotenv()  # Load environment variables first

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.auth import router as auth_router
from app.problems import router as problems_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(auth_router, prefix="/auth")
app.include_router(problems_router, prefix="/api")

@app.get('/ping')
def read_root():
    return {'status': 'ok'}