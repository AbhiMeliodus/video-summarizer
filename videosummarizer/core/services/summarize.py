# summarize.py
from transformers import pipeline
import re
import os

# File paths (centralized here so pipeline.py can import them)
TRANSCRIPT_PATH = os.path.join("downloads", "transcript.txt")
SUMMARY_PATH = os.path.join("downloads", "summary.txt")

# Load model only once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

def clean_text(text):
    """Remove extra whitespace and non-text artifacts."""
    return re.sub(r'\s+', ' ', text).strip()

def chunk_text(text, max_tokens=800):
    """Split transcript into smaller chunks for summarization."""
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks, current = [], ""

    for sent in sentences:
        if len((current + sent).split()) > max_tokens:
            chunks.append(current.strip())
            current = sent + " "
        else:
            current += sent + " "

    if current.strip():
        chunks.append(current.strip())
    return chunks

def summarize_chunk(text):
    """Summarize one chunk using the model."""
    cleaned = clean_text(text)
    result = summarizer(
        cleaned,
        max_length=150,
        min_length=50,
        do_sample=False
    )
    return result[0]["summary_text"].strip()

def summarize_transcript(transcript_file: str, output_file: str = SUMMARY_PATH):
    """
    Summarizes a transcript file into a concise summary and saves it.
    1. Read transcript
    2. Chunk into smaller pieces
    3. Summarize each chunk
    4. Generate final summary
    5. Save to file
    """
    with open(transcript_file, "r", encoding="utf-8") as f:
        transcript = f.read()

    chunks = chunk_text(transcript)
    partial_summaries = []

    for i, chunk in enumerate(chunks):
        partial = summarize_chunk(chunk)
        partial_summaries.append(f"[Chunk {i+1}] {partial}")

    combined_text = "\n".join(partial_summaries)

    # Final summary pass
    final = summarizer(
        f"These are partial summaries of a video transcript:\n\n{combined_text}\n\n"
        "Now write a clear, timestamped bullet-point summary of the key moments in the video. "
        "Format it as [mm:ss] • point.",
        max_length=400,
        min_length=150,
        do_sample=False,
    )[0]["summary_text"].strip()

    # Save summary to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final)

    return final