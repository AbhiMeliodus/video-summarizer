# 🎬 Video Summarizer

A Django web app that takes a YouTube URL and returns a timestamped transcript and chapter-by-chapter summary — powered entirely by the **Groq API** (no local ML models).

## ✨ How It Works

```
YouTube URL → yt-dlp (download audio) → Groq Whisper (transcribe) → Groq LLaMA (summarize) → Results
```

1. **Download** — `yt-dlp` extracts audio as MP3 directly (no intermediate WAV conversion)
2. **Transcribe** — Groq's hosted `whisper-large-v3` produces a timestamped transcript
3. **Summarize** — Transcript is chunked and summarized with `llama-3.1-8b-instant`
4. **Results** — Timestamped transcript + summary displayed and available for download

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5 + Gunicorn |
| Audio download | yt-dlp + ffmpeg |
| Transcription | Groq Whisper API (`whisper-large-v3`) |
| Summarization | Groq LLaMA API (`llama-3.1-8b-instant`) |
| Static files | WhiteNoise |

## 🚀 Run Locally

### Prerequisites
- Python 3.10+
- `ffmpeg` installed on your system ([install guide](https://ffmpeg.org/download.html))
- A [Groq API key](https://console.groq.com) (free)

### Setup

```bash
# Clone the repo
git clone https://github.com/AbhiMeliodus/video-summarizer.git
cd video-summarizer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

# Run
cd videosummarizer
python manage.py collectstatic --noinput
python manage.py runserver
```

Open [http://localhost:8000](http://localhost:8000)

## 🐳 Run with Docker

```bash
# Set your API key
export GROQ_API_KEY=your_key_here

# Build and run
docker compose up --build
```

Open [http://localhost:8080](http://localhost:8080)

## ☁️ Deploy

### Replit (Free, no credit card)
1. Import this repo on [replit.com](https://replit.com)
2. Add `GROQ_API_KEY` in the Secrets panel
3. Run `bash run.sh` in the Shell

### Docker-compatible platforms (Oracle Cloud, self-hosted VPS)
Use the provided `Dockerfile` and `docker-compose.yml`. Set `GROQ_API_KEY` as an environment variable.

## 📁 Project Structure

```
video-summarizer/
├── videosummarizer/          # Django project root
│   ├── core/                 # Main app
│   │   ├── services/
│   │   │   ├── download.py   # yt-dlp audio extraction
│   │   │   ├── transcribe.py # Groq Whisper transcription
│   │   │   ├── summarize.py  # Groq LLaMA summarization
│   │   │   └── pipeline.py   # Orchestrates the full flow
│   │   ├── views.py
│   │   └── urls.py
│   └── templates/            # HTML templates
├── Dockerfile                # Docker image
├── docker-compose.yml        # Docker Compose
├── run.sh                    # Replit startup script
├── replit.nix                # Replit system packages (ffmpeg)
└── requirements.txt
```

## ⚙️ Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key (required) |
| `DJANGO_SECRET_KEY` | Django secret key (auto-generated if not set) |
| `DJANGO_DEBUG` | Set to `True` for development (default: `False`) |
