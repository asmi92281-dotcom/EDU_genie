# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant built with FastAPI and a simple HTML/CSS/JavaScript frontend. It provides:

- Question answering (`/qa`)
- Beginner-friendly concept explanation (`/explain`)
- 3-question MCQ generation (`/quiz`)
- Educational summarization (`/summarize`)
- Beginner-to-advanced learning paths (`/learn/recommendations`)

The original project documentation used Gemini 1.5 Pro and LaMini-Flan-T5. This implementation keeps the same functional architecture but uses the current `google-genai` SDK and a configurable Gemini model. The explanation module also supports the documented LaMini-Flan-T5 model as an optional local backend.

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── schemas.py
├── utils.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    ├── test_utils.py
    └── test_api.py
```

## VS Code setup — Windows

1. Install Python 3.10+.
2. Open this folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

5. Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

6. Copy `.env.example` to `.env` and add your Gemini API key.
7. Start the app:

```powershell
uvicorn main:app --reload
```

8. Open http://127.0.0.1:8000

## macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

## Gemini API key

Create a Gemini API key in Google AI Studio and put it in `.env` as:

```env
GEMINI_API_KEY=your_key_here
```

Never commit `.env` or expose your API key in frontend JavaScript.

## Test

Run:

```bash
pytest -q
```

The tests do not call Gemini. For a live integration test, start the server and try each task from the browser.

## API examples

Health:

```bash
curl http://127.0.0.1:8000/health
```

Question:

```bash
curl -X POST http://127.0.0.1:8000/qa -H "Content-Type: application/json" -d "{\"text\":\"What is photosynthesis?\"}"
```

Quiz:

```bash
curl -X POST http://127.0.0.1:8000/quiz -H "Content-Type: application/json" -d "{\"text\":\"Photosynthesis is the process by which green plants convert light energy into chemical energy.\"}"
```

## Optional local explanation model

The documentation specifies LaMini-Flan-T5-783M for concept explanation. To use it locally:

```bash
pip install -r requirements-local.txt
```

Then set:

```env
EXPLANATION_BACKEND=local
```

The first local explanation request downloads the model from Hugging Face. For the simplest setup, leave `EXPLANATION_BACKEND=gemini`.

## Troubleshooting

- **GEMINI_API_KEY is not configured**: make sure `.env` exists and contains the key, then restart Uvicorn.
- **Model not available**: change `GEMINI_MODEL` to a Gemini model available to your API account.
- **Port already in use**: run `uvicorn main:app --reload --port 8001`.
- **PowerShell blocks activation**: use `py -m venv .venv`, then run `.venv\Scripts\python.exe -m pip install -r requirements.txt` without activating the environment.
