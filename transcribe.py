import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def load_audio_path():
    try:
        with open("downloads/audio_path.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Error: Audio file path not found!")
        return ""


def transcribe_audio(audio_path, output_file="downloads/transcription.txt"):
    """Transcribes audio and adds timestamps using Groq Whisper API."""
    
    with open(audio_path, "rb") as file:
        # Request transcription with timestamp granularities
        transcription = client.audio.transcriptions.create(
          file=(audio_path, file.read()),
          model="whisper-large-v3",
          response_format="verbose_json",
          timestamp_granularities=["segment"]
        )

    # Save transcription with timestamps
    with open(output_file, "w", encoding="utf-8") as f:
        for segment in transcription.segments:
            # Convert start time to mm:ss format
            start_time = segment['start']
            timestamp = f"[{int(start_time // 60)}:{int(start_time % 60):02d}]"
            f.write(f"{timestamp} {segment['text'].strip()}\n")

    return transcription.text


if __name__ == "__main__":
    audio_file = load_audio_path()
    if audio_file:
        transcribed_text = transcribe_audio(audio_file)
        print("✅ Transcription with timestamps saved successfully via Groq!")