# Lightweight Python base — no ML libraries needed, all inference is via Groq API
FROM python:3.10-slim

# Prevent .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install only ffmpeg (the sole system dependency — used by yt-dlp for audio extraction)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip --no-cache-dir \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Create non-root user and ensure downloads dir is writable
RUN useradd -m appuser \
    && mkdir -p /app/videosummarizer/downloads \
    && chown -R appuser:appuser /app

WORKDIR /app/videosummarizer

USER appuser

# Collect static files (WhiteNoise serves them — no separate nginx needed)
RUN python manage.py collectstatic --noinput

EXPOSE 8080

# Single worker — safe for 256MB Koyeb free tier.
# Timeout 120s — yt-dlp + Groq transcription can take ~30-60s on long videos.
CMD ["gunicorn", "videosummarizer.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "1", "--timeout", "120", "--keep-alive", "5"]