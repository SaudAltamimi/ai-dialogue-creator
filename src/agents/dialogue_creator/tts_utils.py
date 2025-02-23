from openai import OpenAI
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List
from .dialogue_creator_agent import Podcast, DialogueLine

@dataclass
class TTSConfig:
    base_url: str = "http://localhost:8880/v1"
    api_key: str = "not-needed"
    model: str = "kokoro"
    male_voice: str = "bm_fable"  # Voice for male speakers
    female_voice: str = "bf_v0isabella"  # Voice for female speakers
    output_dir: Path = Path("output")

class TextToSpeechService:
    def __init__(self, config: Optional[TTSConfig] = None):
        self.config = config or TTSConfig()
        self.client = self._create_client()
        self._ensure_output_dir()
    
    def _create_client(self) -> OpenAI:
        return OpenAI(
            base_url=self.config.base_url,
            api_key=self.config.api_key
        )
    
    def _ensure_output_dir(self):
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_speech(self, text: str, voice: Optional[str] = None, output_path: Optional[Path] = None) -> str:
        if output_path is None:
            output_path = self.config.output_dir / f"{hash(text)}.mp3"
        else:
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with self.client.audio.speech.with_streaming_response.create(
            model=self.config.model,
            voice=voice or self.config.male_voice,  # Default to male voice if not specified
            input=text
        ) as response:
            response.stream_to_file(str(output_path))
        
        return str(output_path)


class DialogueToSpeech:
    def __init__(self, output_base_dir: Path = Path("output/podcasts")):
        self.tts_service = get_tts_service()
        self.output_base_dir = output_base_dir
        self.output_base_dir.mkdir(parents=True, exist_ok=True)

    def _sanitize_filename(self, text: str) -> str:
        """Convert text to safe filename."""
        return "".join(c if c.isalnum() else "_" for c in text).lower()

    def generate_podcast_audio(self, podcast: Podcast) -> List[Path]:
        """Generate audio files for each podcast part."""
        audio_files = []
        
        for i, part in enumerate(podcast.parts, 1):
            # Create directory for this part
            part_dir = self.output_base_dir / f"part_{i}_{self._sanitize_filename(part.title)}"
            part_dir.mkdir(exist_ok=True)
            
            # Generate audio for each dialogue line with appropriate voice
            for j, line in enumerate(part.dialogue):
                output_path = part_dir / f"line_{j}.mp3"
                voice = self.tts_service.config.female_voice if line.speaker_gender == "female" else self.tts_service.config.male_voice
                self.tts_service.generate_speech(
                    text=line.content,
                    voice=voice,
                    output_path=output_path
                )
                audio_files.append(output_path)
            
        return audio_files

    def combine_podcast_parts(self, podcast: Podcast) -> Path:
        """Combine all podcast parts into a single audio file."""
        from pydub import AudioSegment

        # Generate individual audio files first
        part_files = self.generate_podcast_audio(podcast)
        
        # Combine all parts
        combined = AudioSegment.empty()
        for audio_file in part_files:
            part_audio = AudioSegment.from_mp3(audio_file)
            combined += part_audio
            # Add a short pause between lines
            combined += AudioSegment.silent(duration=500)
        
        # Save combined file
        output_path = self.output_base_dir / "full_podcast.mp3"
        combined.export(output_path, format="mp3")
        
        return output_path

def get_tts_service(config: Optional[TTSConfig] = None) -> TextToSpeechService:
    return TextToSpeechService(config)

if __name__ == "__main__":
    tts = get_tts_service()
    output_file = tts.generate_speech("Hello world!")
    print(f"Audio saved to: {output_file}")