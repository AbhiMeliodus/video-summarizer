import os
import re
import warnings
from datetime import timedelta
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# Suppress warnings
warnings.filterwarnings("ignore")

# Use a reliable summarization model
model_name = "facebook/bart-large-cnn"
print("🔄 Loading summarization model...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

TRANSCRIPT_PATH = "downloads/transcription.txt"
SUMMARY_PATH = "downloads/transcription_summary.txt"

def load_transcript(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def clean_line(line):
    # Remove timestamps and speaker tags like "[0:01]" or "Speaker 1:"
    line = re.sub(r"\[\d+:\d+\]", "", line)
    line = re.sub(r"(Speaker\s*\d+:)", "", line, flags=re.IGNORECASE)
    return line.strip()

def extract_timestamp(raw_line):
    # Find timestamp like [3:45] or [12:07]
    match = re.search(r"\[(\d+):(\d+)\]", raw_line)
    if match:
        minutes, seconds = map(int, match.groups())
        return str(timedelta(minutes=minutes, seconds=seconds))
    return "??:??"

def chunk_transcript(lines, max_words=120):
    chunks = []
    timestamps = []
    current_chunk = []
    word_count = 0
    last_timestamp = "??:??"

    for line in lines:
        if not line.strip():
            continue

        ts = extract_timestamp(line)
        text = clean_line(line)

        if len(text.split()) < 4:
            continue  # skip short/filler lines

        if not current_chunk:
            last_timestamp = ts  # start timestamp of this chunk

        current_chunk.append(text)
        word_count += len(text.split())

        if word_count >= max_words:
            chunks.append(" ".join(current_chunk))
            timestamps.append(last_timestamp)
            current_chunk = []
            word_count = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))
        timestamps.append(last_timestamp)

    return chunks, timestamps

def summarize_chunks(chunks, timestamps):
    summaries = []
    for idx, chunk in enumerate(chunks):
        try:
            summary = summarizer(chunk, max_length=130, min_length=40, do_sample=False)[0]['summary_text']
            summaries.append((timestamps[idx], summary))
        except Exception as e:
            print(f"⚠️ Skipped chunk {idx+1} due to error: {e}")
    return summaries

def print_and_save(summaries, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        print("\n✅ Summary:\n")
        for timestamp, summary in summaries:
            line = f"[{timestamp}] • {summary}"
            print(line)
            f.write(line + "\n")

if __name__ == "__main__":
    print("🧠 Summarizing transcript...")

    if not os.path.exists(TRANSCRIPT_PATH):
        print("❌ Transcript not found.")
        exit(1)

    transcript_lines = load_transcript(TRANSCRIPT_PATH)
    chunks, timestamps = chunk_transcript(transcript_lines)
    summaries = summarize_chunks(chunks, timestamps)
    print_and_save(summaries, SUMMARY_PATH)
    print(f"\n📄 Saved summary to: {SUMMARY_PATH}")