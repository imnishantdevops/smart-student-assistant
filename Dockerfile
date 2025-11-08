# ===== Base image =====
FROM python:3.12-slim

# ===== Set environment variables =====
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ===== Set working directory =====
WORKDIR /app

# ===== System dependencies =====
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# ===== Copy project files =====
COPY backend ./backend
COPY frontend ./frontend
COPY requirements.txt ./requirements.txt

# ===== Install Python dependencies =====
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install streamlit fastapi uvicorn

# ===== Expose ports =====
EXPOSE 8000 8501

# ===== Start both backend and frontend =====
# You can use supervisord or a simple bash command to run both
CMD bash -c "uvicorn backend.app:app --host 0.0.0.0 --port 8000 & \
             streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0"
