Smart Student Assistant

The Smart Student Assistant is an AI-powered tool designed to help students convert handwritten notes into editable text, summarize long passages, and ask questions directly from their notes. It combines OCR, summarization, and question answering in a single, easy-to-use web interface.

Overview

This project integrates multiple NLP and CV models into a unified system. The backend exposes REST APIs using FastAPI, while the frontend provides a simple and interactive interface built with Streamlit.

The goal is to make studying more efficient by helping students quickly extract, understand, and interact with their content.

Features

Handwriting OCR – Extracts text from handwritten images using Tesseract OCR

Summarization – Generates concise summaries of long text using BART (facebook/bart-large-cnn)

Question Answering – Fine-tuned DistilBERT on the SQuAD dataset to answer questions based on user-provided text

FastAPI Backend – REST endpoints for QA, summarization, and OCR

Streamlit Frontend – Simple interface for uploading notes, asking questions, and viewing results

LLMOps Logging – Records latency, input/output size, and success metrics in JSONL format

Architecture
User (Streamlit UI)
       │
       ▼
FastAPI Backend
 ├── Question Answering (DistilBERT)
 ├── Summarization (BART)
 ├── OCR (Tesseract)
 └── Logging (backend/logs/requests.log)
 
Model Fine-tuning

DistilBERT was fine-tuned on a subset of the SQuAD dataset using Google Colab.

The trained model is stored in backend/models/distilbert-qa-final/.

If the fine-tuned model is not found, the backend automatically loads a fallback model (roberta-base-squad2).

LLMOps Logging

Each API request is logged in backend/logs/requests.log with details such as endpoint, latency, input/output size, and success status.

Example log entry:

{
  "endpoint": "/qa",
  "question": "What are the three service models in cloud computing?",
  "context_length": 198,
  "answer": "IaaS, PaaS, SaaS",
  "latency": 0.0743,
  "success": true
}
Example Use Cases

Upload a handwritten image to extract clean text.

Paste a long passage and generate a short summary.

Ask questions like “What are the key takeaways?” from your notes and get an instant answer.

Future Enhancements

Fine-tune QA models on domain-specific datasets

Add evaluation metrics such as EM and F1

Optimize models through pruning or quantization

Containerize and deploy using Docker or Kubernetes

Conclusion

The Smart Student Assistant demonstrates how AI and NLP models can be integrated into cloud-native applications.
It provides a practical example of the complete machine learning lifecycle — from data preparation and model training to deployment, monitoring, and evaluation.
