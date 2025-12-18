import yt_dlp
import tempfile
import uuid
import os

class YouTubeService:
    """
    Service class for downloading audio from YouTube videos.

    This class provides functionality to:
    - Download audio from a given YouTube URL
    - Convert the audio to MP3 format
    - Return the local file path and video metadata

    Example usage:
        audio_file, info = YouTubeService.download_audio("https://youtu.be/...")
    """

    @staticmethod
    def download_audio(url: str) -> tuple[str, dict]:
        """
        Download the audio from a YouTube video as MP3.

        The audio is downloaded to a temporary directory with a
        unique filename. Only the first video is processed if the
        URL points to a playlist.

        Args:
            url (str): The full YouTube video URL to download.

        Returns:
            tuple[str, dict]: A tuple containing:
                - The local path to the downloaded MP3 file
                - The metadata dictionary returned by yt_dlp

        Raises:
            RuntimeError: If the audio file could not be downloaded
                          or created.
        """
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
