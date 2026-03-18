# Use Python 3.10-slim (Supports ARM64 and AMD64)
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Create a non-root user for Choreo
# Choreo often requires a user with a specific UID range (10000-20000)
RUN useradd -u 10014 choreo-user
RUN chown -R 10014:10014 /app

# Switch to the non-root user
USER 10014

# Collect static files
RUN python videosummarizer/manage.py collectstatic --noinput

# Expose port
EXPOSE 8080

# Run Gunicorn
CMD ["sh", "-c", "gunicorn videosummarizer.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 2"]