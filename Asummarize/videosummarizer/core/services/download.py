import yt_dlp
import ffmpeg
import os

def download_video(url, output_dir="downloads"):
    """Downloads video using yt-dlp and returns WAV filename"""
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192"
        }],
        "restrictfilenames": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        wav_file = os.path.splitext(filename)[0] + ".wav"
        return wav_file

def convert_to_mp3(wav_audio, mp3_audio):
    """Converts WAV to MP3 using ffmpeg"""
    wav_audio = os.path.abspath(wav_audio)
    mp3_audio = os.path.abspath(mp3_audio)
    ffmpeg.input(wav_audio).output(
        mp3_audio, format="mp3", audio_bitrate="128k"
    ).run(overwrite_output=True)
    os.remove(wav_audio)  # Remove temporary WAV file

def download_audio(url):
    """Full process: Download video, extract audio, convert to MP3"""
    wav_file = download_video(url)
    mp3_file = wav_file.replace(".wav", ".mp3")
    convert_to_mp3(wav_file, mp3_file)
    return mp3_file


if __name__ == "__main__":
    video_url = input("Enter YouTube video URL: ").strip()
    audio_file = download_audio(video_url)

    with open("downloads/audio_path.txt", "w", encoding="utf-8") as f:
        f.write(audio_file)

    print(f"✅ Audio saved successfully: {audio_file}")