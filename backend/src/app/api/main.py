from contextlib import asynccontextmanager

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.api.v1.router import router as v1_router
from src.app.utils.helper import get_db_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("-> Starting application...")
    load_dotenv(find_dotenv(), override=True)
    db = get_db_engine()
    await db.init()
    print("-> DB Connected Successfully ✅")
    yield
    await db.close()
    print("Shutting down application...")


app = FastAPI(title="Chatbot Builder", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix="/api/v1")


@app.get("/")
async def index():
    return {"Hi": "Dear User"}


@app.get("/health")
async def health():
    return {"status": "ok"}
