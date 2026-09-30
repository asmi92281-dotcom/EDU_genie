from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from schemas import TextRequest, QuizResponse
from explanation_module import explain_topic
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent
settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0", description="Gemini-powered educational learning assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.cors_origins.split(",") if x.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )

@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name, "model": settings.gemini_model}

@app.post("/qa")
def qa(payload: TextRequest):
    return {"result": answer_question(payload.text)}

@app.post("/explain")
def explain(payload: TextRequest):
    return {"result": explain_topic(payload.text)}

@app.post("/quiz", response_model=QuizResponse)
def quiz(payload: TextRequest):
    return generate_quiz(payload.text)

@app.post("/summarize")
def summarize(payload: TextRequest):
    return {"result": summarize_text(payload.text)}

@app.post("/learn/recommendations")
def recommendations(payload: TextRequest):
    return {"result": get_learning_recommendations(payload.text)}

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=500, content={"detail": str(exc)})
