from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth.signup import router as signup_router
from routes.auth.login import router as login_router
from routes.home.translate_and_transcribe import app as translate_transcribe_router
from routes.home.translate_text import app as translate_text_router
from routes.home.text_to_speech import app as text_to_speech_router

app = FastAPI()

# CORS setup
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Include routers
app.include_router(signup_router, prefix="/signup", tags=["Auth"])
app.include_router(login_router, prefix="/login", tags=["Auth"])

# Combine translate routes into a single router
app.include_router(translate_transcribe_router, prefix="/app", tags=["Transcribe and Translate"])
app.include_router(translate_text_router, prefix="/app", tags=["Translate"]) 
app.include_router(text_to_speech_router, prefix="/app", tags=["Text to Speech"])  