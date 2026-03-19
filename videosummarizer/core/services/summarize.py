import os
import re
from datetime import timedelta
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

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
            continue

        if not current_chunk:
            last_timestamp = ts

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
    print(f"🧠 Summarizing {len(chunks)} chunks using Groq API...")
    for idx, chunk in enumerate(chunks):
        try:
            prompt = f"Summarize the following transcript segment. Be concise but maintain all key points. Do not add conversational intro/outro text:\n\n{chunk}"
            
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a professional video summarizer. Provide concise, direct summaries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=150,
            )
            
            summary = completion.choices[0].message.content.strip()
            summaries.append((timestamps[idx], summary))
        except Exception as e:
            print(f"⚠️ Skipped chunk {idx+1} due to error: {e}")
    return summaries

def summarize_transcript(transcript_file, output_file=None):
    """
    Summarize the transcript via Groq API.
    """
    transcript_lines = load_transcript(transcript_file)
    chunks, timestamps = chunk_transcript(transcript_lines)
    summaries = summarize_chunks(chunks, timestamps)
    
    summary_text = ""
    for timestamp, summary in summaries:
        summary_text += f"[{timestamp}] • {summary}\n"
        
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(summary_text)

    return summary_text