import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def transcribe_audio(audio_path, output_file="downloads/transcription.txt"):
    """Transcribes audio and adds timestamps using Groq Whisper API."""

    with open(audio_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(audio_path, file.read()),
            model="whisper-large-v3",
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )

    # Save transcription with timestamps
    with open(output_file, "w", encoding="utf-8") as f:
        for segment in transcription.segments:
            start_time = segment['start']
            timestamp = f"[{int(start_time // 60)}:{int(start_time % 60):02d}]"
            f.write(f"{timestamp} {segment['text'].strip()}\n")

    return transcription.text