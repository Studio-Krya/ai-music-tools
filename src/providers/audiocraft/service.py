"""Service layer for Audiocraft audio generation."""
from pathlib import Path
from typing import Dict
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile

from src.providers.audiocraft.dtos import MusicGenParams
from src.providers.base import get_default_output


class AudiocraftService:
    _models: Dict[str, MusicgenForConditionalGeneration] = {}
    _processors: Dict[str, AutoProcessor] = {}

    def initialize_model(self, model_name: str = "facebook/musicgen-small"):
        if model_name not in self._models:
            self._models[model_name] = MusicgenForConditionalGeneration.from_pretrained(model_name)
            self._processors[model_name] = AutoProcessor.from_pretrained(model_name)
        return self._models[model_name], self._processors[model_name]

    def generate_music(self, params: MusicGenParams) -> Path:
        model, processor = self.initialize_model(params.model)

        if params.output:
            output_path = get_default_output("audiocraft", params.output)
        else:
            output_path = get_default_output("audiocraft")

        max_tokens = 60 * params.duration
        print("Generating music...")

        inputs = processor(
            text=[params.prompt],
            padding=True,
            return_tensors="pt",
        )

        audio_values = model.generate(
            **inputs, 
            do_sample=True,
            max_new_tokens=max_tokens,
            guidance_scale=3.0
        )

        sampling_rate = model.config.audio_encoder.sampling_rate
        scipy.io.wavfile.write(output_path, rate=sampling_rate, data=audio_values[0, 0].numpy())

        return output_path

    # def generate_audio(params: AudioGenParams) -> Path:
    #     """Generate audio from text prompt using AudioGen.
        
    #     Args:
    #         params: AudioGen generation parameters
            
    #     Returns:
    #         Path to the generated audio file
            
    #     Raises:
    #         ImportError: If audiocraft is not installed
    #         Exception: If generation fails
    #     """
    #     try:
    #         from audiocraft.models import AudioGen
    #         import torchaudio
    #     except ImportError as e:
    #         raise ImportError(f"Error importing audiocraft: {e}") from e
        
    #     # Determine output path
    #     if params.output:
    #         output_path = Path(params.output)
    #     else:
    #         output_path = get_default_output("audiocraft", "output.wav")
        
    #     output_path.parent.mkdir(parents=True, exist_ok=True)
        
    #     # Load model
    #     model_obj = AudioGen.get_pretrained(params.model)
        
    #     # Set generation parameters
    #     model_obj.set_generation_params(duration=params.duration)
        
    #     # Generate audio
    #     wav = model_obj.generate([params.prompt])
        
    #     # Save audio
    #     torchaudio.save(str(output_path), wav[0].cpu(), model_obj.sample_rate)
        
    #     return output_path
