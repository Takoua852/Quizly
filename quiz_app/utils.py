from urllib.parse import urlparse, parse_qs

def extract_video_id(url: str) -> str | None:
    """
    Extract the YouTube video ID from different URL formats.

    Supported formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID

    Args:
        url (str): Raw YouTube URL provided by the client.

    Returns:
        str | None: Video ID if valid, otherwise None.
    """
    parsed = urlparse(url)

    if "youtube.com" in parsed.netloc:
        return parse_qs(parsed.query).get("v", [None])[0]

    if "youtu.be" in parsed.netloc:
        return parsed.path.lstrip("/")

    return None