# backend/app.py

import os, time, json, io
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import pytesseract
from transformers import pipeline

# =========================
# CONFIG
# =========================
app = FastAPI(title="Smart Student Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

os.makedirs("logs", exist_ok=True)
LOG_PATH = "logs/requests.log"

def log_event(entry):
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")


# =========================
# LOAD FREE HUGGINGFACE MODELS
# =========================

print("Loading HuggingFace models... please wait...")

qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

print("Models loaded ✅")

# =========================
# DATA MODELS
# =========================
class QARequest(BaseModel):
    context: str
    question: str


# =========================
# ENDPOINTS
# =========================

@app.get("/health")
async def health():
    return {"status": "ok"}


# Question Answering
@app.post("/qa")
async def qa(req: QARequest, request: Request):
    start = time.time()
    try:
        result = qa_model(question=req.question, context=req.context)
        answer = result["answer"]
        success = True
    except Exception as e:
        answer = f"Error: {str(e)}"
        success = False

    latency = time.time() - start
    log_event({
        "endpoint": "/qa",
        "question": req.question,
        "context_length": len(req.context),
        "answer": answer,
        "latency": latency,
        "success": success
    })
    return {"answer": answer}


# Summarization
@app.post("/summarize")
async def summarize(data: dict):
    text = data.get("text", "")
    start = time.time()

    try:
        summary = summarizer(text, max_length=120, min_length=30, do_sample=False)[0]["summary_text"]
        success = True
    except Exception as e:
        summary = f"Error: {str(e)}"
        success = False

    latency = time.time() - start
    log_event({
        "endpoint": "/summarize",
        "input_length": len(text),
        "summary": summary,
        "latency": latency,
        "success": success
    })
    return {"summary": summary}


# Handwriting OCR
@app.post("/hw-eval")
async def handwriting_eval(file: UploadFile = File(...)):
    start = time.time()

    # Read image
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    # OCR extract text
    extracted_text = pytesseract.image_to_string(image)

    latency = time.time() - start
    log_event({
        "endpoint": "/hw-eval",
        "file_size": len(image_bytes),
        "text_length": len(extracted_text),
        "latency": latency,
        "success": True
    })

    return {"extracted_text": extracted_text}
