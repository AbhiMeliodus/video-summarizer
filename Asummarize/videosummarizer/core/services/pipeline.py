import os
import time
import shutil
from core.services.download import download_audio
from core.services.transcribe import transcribe_audio
from core.services.summarize import summarize_transcript

# ✅ Use /tmp directory because /app is read-only in Hugging Face
DOWNLOADS_DIR = "/tmp/downloads"
TRANSCRIPT_PATH = os.path.join(DOWNLOADS_DIR, "transcript.txt")
SUMMARY_PATH = os.path.join(DOWNLOADS_DIR, "summary.txt")


def wait_for_file(path, timeout=30):
    """Wait until file exists (handles ffmpeg delay)."""
    start = time.time()
    while not os.path.exists(path):
        if time.time() - start > timeout:
            raise FileNotFoundError(f"Audio file not found after {timeout}s: {path}")
        time.sleep(0.5)
    return path


def clean_downloads():
    """Deletes everything inside the downloads folder."""
    if os.path.exists(DOWNLOADS_DIR):
        shutil.rmtree(DOWNLOADS_DIR)
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)


def run_pipeline(youtube_url: str):
    """
    End-to-end pipeline:
    1. Download audio
    2. Wait until audio file exists
    3. Transcribe audio to text
    4. Summarize transcript
    5. Return paths to transcript + summary
    """
    clean_downloads()

    # 1. Download audio
    print(f"\n🎥 Downloading audio from: {youtube_url}")
    audio_path = download_audio(youtube_url)

    # 2. Ensure audio file exists before transcription
    audio_path = wait_for_file(audio_path)

    # 3. Transcribe
    print("\n📝 Transcribing audio...")
    transcribe_audio(audio_path, output_file=TRANSCRIPT_PATH)

    # 4. Summarize
    print("\n🧠 Summarizing transcript...")
    summarize_transcript(TRANSCRIPT_PATH, output_file=SUMMARY_PATH)

    # 5. Return output paths
    print(f"\n📄 Transcript: {TRANSCRIPT_PATH}")
    print(f"📄 Summary: {SUMMARY_PATH}")
    return TRANSCRIPT_PATH, SUMMARY_PATH