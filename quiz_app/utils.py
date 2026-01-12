from urllib.parse import urlparse, parse_qs

def extract_video_id(url: str) -> str | None:

    """Extract the video ID from a YouTube URL (youtube.com or youtu.be)."""
    
    parsed = urlparse(url)

    if "youtube.com" in parsed.netloc:
        return parse_qs(parsed.query).get("v", [None])[0]

    if "youtu.be" in parsed.netloc:
        return parsed.path.lstrip("/")

    return None