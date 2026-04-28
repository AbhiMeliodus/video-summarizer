import os
import re
from transformers import pipeline

# Paths for pipeline.py
BASE_DIR = "downloads"
TRANSCRIPT_PATH = os.path.join(BASE_DIR, "transcript.txt")
SUMMARY_PATH = os.path.join(BASE_DIR, "summary.txt")

# Load summarizer once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def chunk_text(text, max_tokens=1000):
    """
    Splits transcript into chunks that fit the model context window.
    """
    words = text.split()
    chunks, current = [], []

    for word in words:
        current.append(word)
        if len(current) >= max_tokens:
            chunks.append(" ".join(current))
            current = []
    if current:
        chunks.append(" ".join(current))

    return chunks


def summarize_chunk(text):
    """
    Summarize a single chunk of text.
    """
    summary = summarizer(
        text,
        max_length=150,
        min_length=60,
        do_sample=False,
    )
    return summary[0]["summary_text"]


def clean_summary(text: str) -> str:
    """
    Removes leftover instructions or repeated phrases from the summary.
    """
    # Kill common prompt echoes
    text = re.sub(r"(Now write.*|Do not.*|Summarize.*|Here is.*)", "", text, flags=re.IGNORECASE)

    # Normalize whitespace
    return re.sub(r"\s+", " ", text).strip()


def summarize_transcript(transcript_file, output_file=None):
    """
    Summarize the transcript into a clean, concise paragraph.
    """
    # 1. Load transcript
    with open(transcript_file, "r", encoding="utf-8") as f:
        transcript_text = f.read().strip()

    # 2. Break into chunks
    chunks = chunk_text(transcript_text)

    # 3. Summarize each chunk
    partial_summaries = [summarize_chunk(chunk) for chunk in chunks]

    # 4. Merge partials and re-summarize (NO instructions this time)
    merged_text = " ".join(partial_summaries)
    final = summarizer(
        merged_text,
        max_length=300,
        min_length=100,
        do_sample=False,
    )
    summary_text = clean_summary(final[0]["summary_text"])

    # 5. Save if requested
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(summary_text)

    return summary_text


# Debug run
if __name__ == "__main__":
    if os.path.exists(TRANSCRIPT_PATH):
        summary = summarize_transcript(TRANSCRIPT_PATH, SUMMARY_PATH)
        print("\n✅ Final Summary:\n")
        print(summary)
    else:
        print("❌ Transcript file not found. Run transcription first.")