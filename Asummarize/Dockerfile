# Use Python 3.12
FROM python:3.12-slim

# Environment setup
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Django settings
ENV DJANGO_SETTINGS_MODULE=videosummarizer.settings
# ✅ Redirect HF cache to a writable path
ENV HF_HOME=/app/cache
ENV TRANSFORMERS_CACHE=/app/cache
ENV HUGGINGFACE_HUB_CACHE=/app/cache

# Work directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Install requirements
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy code
COPY . /app/

# ✅ Create cache directory with safe permissions
RUN mkdir -p /app/cache && chmod -R 777 /app/cache

# Debug folder tree
RUN ls -R /app/videosummarizer

# Move into folder with manage.py
WORKDIR /app/videosummarizer

RUN mkdir -p /app/videosummarizer/downloads && chmod -R 777 /app/videosummarizer/downloads

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 7860

# ✅ Launch Gunicorn
CMD ["gunicorn", "videosummarizer.wsgi:application", "--bind", "0.0.0.0:7860", "--workers", "2"]