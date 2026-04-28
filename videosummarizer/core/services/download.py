import yt_dlp
import os

def download_audio(url, output_dir=None):
    """
    Downloads audio from a YouTube URL and returns the MP3 file path.
    Uses yt-dlp's built-in FFmpeg postprocessor to extract audio directly
    as MP3 in one step — avoids the double WAVMP3 conversion.
    """
    if output_dir is None:
        output_dir = "downloads"

    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "96",   # 96kbps — fine for speech, ~10MB per 10min
        }],
        "restrictfilenames": True,
        "noplaylist": True,             # Never accidentally download a full playlist
        "extractor_args": {
            "youtube": {
                "player_client": ["default", "-android_sdkless"]
            }
        },
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        # yt-dlp postprocessor renames the file to .mp3
        mp3_file = os.path.splitext(filename)[0] + ".mp3"
        return mp3_file