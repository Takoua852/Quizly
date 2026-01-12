import yt_dlp
import tempfile
import uuid
import os

class YouTubeService:
    """Service to download audio from YouTube videos as MP3 with metadata."""


    @staticmethod
    def download_audio(url: str) -> tuple[str, dict]:
        """Download a YouTube video's audio as MP3 and return file path and metadata."""

        tmp_dir = tempfile.gettempdir()
        filename = os.path.join(tmp_dir, f"{uuid.uuid4()}.%(ext)s")

        ydl_opts = {
            "format": "bestaudio[ext=m4a]/bestaudio/best",
            "outtmpl": filename,
            "quiet": True,
            "noplaylist": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            audio_file = (
                ydl.prepare_filename(info)
                .replace(".webm", ".mp3")
                .replace(".m4a", ".mp3")
            )

        if not os.path.exists(audio_file):
            raise RuntimeError("Audio-Download fehlgeschlagen")

        return audio_file, info
