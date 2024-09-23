from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth.signup import router as signup_router
from routes.auth.login import router as login_router
from routes.home.translate_and_transcribe import app as translate_transcribe_router
from routes.home.translate_text import app as translate_text_router  # Importing the translate_text router

app = FastAPI()

# CORS setup
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(signup_router, prefix="/signup", tags=["Auth"])
app.include_router(login_router, prefix="/login", tags=["Auth"])

# Combine translate routes into a single router
app.include_router(translate_transcribe_router, prefix="/app", tags=["Transcribe and Translate"])
app.include_router(translate_text_router, prefix="/app", tags=["Translate"])  # Avoid conflict
