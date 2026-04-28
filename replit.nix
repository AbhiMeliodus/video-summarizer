{ pkgs }: {
  deps = [
    pkgs.ffmpeg          # Required by yt-dlp for audio extraction
    pkgs.python310       # Python runtime
    pkgs.python310Packages.pip
  ];
}
