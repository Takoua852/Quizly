import whisper

class TranscriptionService:
    """
    Service class for transcribing audio files into text using
    OpenAI's Whisper model.

    Responsibilities:
    - Load the Whisper model
    - Transcribe a given audio file to text
    - Return the plain transcription as a string

    Example usage:
        text = TranscriptionService.transcribe("/path/to/audio.mp3")
    """

    @staticmethod
    def transcribe(audio_file: str) -> str:
        """
        Transcribe an audio file to text using the Whisper 'tiny' model.

        Args:
            audio_file (str): Path to the local audio file to transcribe.

        Returns:
            str: The transcribed text.

        Raises:
            Any exceptions raised by the Whisper library during
            model loading or transcription will propagate.
        """
        model = whisper.load_model("tiny")
        result = model.transcribe(audio_file)
        return result["text"]
