import whisper

class TranscriptionService:

    """Service to transcribe audio files into text using Whisper."""

    @staticmethod
    def transcribe(audio_file: str) -> str:
        """Transcribe an audio file to plain text using the 'tiny' Whisper model."""

        model = whisper.load_model("tiny")
        result = model.transcribe(audio_file)
        return result["text"]
