import whisper

def load_audio_path():
    try:
        with open("downloads/audio_path.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Error: Audio file path not found!")
        return ""
    
def transcribe_audio(audio_path, output_file="downloads/transcription.txt"):
    """Transcribes audio and adds timestamps in mm:ss format."""
    model = whisper.load_model("medium")  # You can change to "tiny", "small", "large"
    
    # Enable word-level timestamps for precise tracking
    result = model.transcribe(audio_path, word_timestamps=True)

    # Save transcription with timestamps
    with open(output_file, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            # Convert start time to mm:ss format
            timestamp = f"[{int(segment['start'] // 60)}:{int(segment['start'] % 60):02d}]"
            f.write(f"{timestamp} {segment['text']}\n")

    return result["text"]


audio_file = load_audio_path()
if audio_file:
    transcribed_text = transcribe_audio(audio_file)
    print("✅ Transcription with timestamps saved successfully!")