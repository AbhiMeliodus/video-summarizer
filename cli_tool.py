# main.py

import os
import shutil
from download import download_audio
from transcribe import transcribe_audio
from summarize import (
    load_transcript,
    chunk_transcript,
    summarize_chunks,
    print_and_save,
    SUMMARY_PATH,
    TRANSCRIPT_PATH,
)

DOWNLOADS_DIR = "downloads"


def clean_downloads():
    """Deletes everything inside the downloads folder"""
    if os.path.exists(DOWNLOADS_DIR):
        shutil.rmtree(DOWNLOADS_DIR)
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)


def run_pipeline(youtube_url):
    print(f"\n🎥 Downloading audio from: {youtube_url}")
    audio_path = download_audio(youtube_url)

    # Save audio path for transcribe.py
    with open(f"{DOWNLOADS_DIR}/audio_path.txt", "w", encoding="utf-8") as f:
        f.write(audio_path)

    print("\n📝 Transcribing audio...")
    transcribe_audio(audio_path, output_file=TRANSCRIPT_PATH)

    print("\n🧠 Summarizing transcript...")
    transcript_lines = load_transcript(TRANSCRIPT_PATH)
    chunks, timestamps = chunk_transcript(transcript_lines)
    summaries = summarize_chunks(chunks, timestamps)
    print_and_save(summaries, SUMMARY_PATH)

    print(f"\n📄 Transcript saved to: {TRANSCRIPT_PATH}")
    print(f"📄 Summary saved to: {SUMMARY_PATH}\n")


def main():
    print("🧠 Welcome to the YouTube Summarizer!")

    while True:
        url = input("🔗 Enter a YouTube video URL (or 'q' to quit): ").strip()
        if url.lower() in {"q", "quit", "exit"}:
            break

        clean_downloads()  # clean only before a new run

        try:
            run_pipeline(url)
        except Exception as e:
            print(f"\n❌ Error processing video: {e}")

        again = input("\n🔁 Do you want to summarize another video? (y/n): ").strip().lower()
        if again != 'y':
            break

    # Instead of deleting, ask user
    delete = input("\n🧹 Do you want to delete all session files? (y/n): ").strip().lower()
    if delete == "y":
        clean_downloads()
        print("✅ Session files removed.")
    else:
        print(f"📂 Files are available in the '{DOWNLOADS_DIR}' folder.")


if __name__ == "__main__":
    main()