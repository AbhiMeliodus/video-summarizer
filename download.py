import yt_dlp
import ffmpeg
import os

def download_video(url, output_dir="downloads"):
    """Downloads video using yt-dlp and returns filename"""
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",  # Convert Opus to WAV first
            "preferredquality": "192"
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return f"{output_dir}/{info['title']}.wav"  # Return WAV filename

def convert_to_mp3(wav_audio, mp3_audio):
    """Converts WAV to MP3 using ffmpeg"""
    ffmpeg.input(wav_audio).output(mp3_audio, format="mp3", audio_bitrate="128k").run()
    os.remove(wav_audio)  # Remove temporary WAV file

def download_audio(url):
    """Full process: Download video, extract audio, convert to MP3"""
    wav_file = download_video(url)
    mp3_file = wav_file.replace(".wav", ".mp3")
    convert_to_mp3(wav_file, mp3_file)
    return mp3_file


video_url = input("Enter YouTube video URL: ").strip()
audio_file = download_audio(video_url)

# Save the downloaded audio path for later use
with open("downloads/audio_path.txt", "w", encoding="utf-8") as f:
    f.write(audio_file)
    
print(f"✅ Audio saved successfully: {audio_file}")