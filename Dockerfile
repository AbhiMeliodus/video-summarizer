# Use Python 3.10 (Hugging Face supports it well)
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (ffmpeg needed for whisper)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files
RUN python videosummarizer/manage.py collectstatic --noinput

# Expose port
EXPOSE 7860

# Run Gunicorn (Django entry point)
CMD ["gunicorn", "videosummarizer.wsgi:application", "--bind", "0.0.0.0:7860", "--workers", "2"]