
from typing import Dict
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile
import torch

from src.utils.file import get_folder_output
from src.utils.transformers import BaseProgressStreamer

from .dtos import MusicGenParams

TOKENS_PER_SECOND = 52.0
CHUNK_SIZE = 750

class AudiocraftService:
    _models: Dict[str, MusicgenForConditionalGeneration] = {}
    _processors: Dict[str, AutoProcessor] = {}
    _device: torch.device = torch.device("cpu")

    def initialize_model(self, model_name: str = "facebook/musicgen-small"):
        if model_name not in self._models:
            # Check if GPU is available
            if torch.cuda.is_available():
                self._device = torch.device("cuda")
            
            print(f"Initializing model: {model_name}")
            self._models[model_name] = MusicgenForConditionalGeneration.from_pretrained(model_name)
            self._processors[model_name] = AutoProcessor.from_pretrained(model_name)
            
            # self._models[model_name] = self._models[model_name].to(torch.bfloat16)

        return self._models[model_name], self._processors[model_name]

    def unload_model(self, model_name: str):
        if model_name in self._models:
            del self._models[model_name]
            del self._processors[model_name]

    def generate_music(self, params: MusicGenParams) -> str:
        output_path = get_folder_output("audiocraft")
        model, processor = self.initialize_model(params.model)

        max_tokens = int(TOKENS_PER_SECOND * params.duration)
        
        model = model.to(torch.bfloat16)

        inputs = processor(
            text=[params.prompt],
            padding=True,
            return_tensors="pt",
        )

        model.to(self._device)
        inputs = {k: v.to(self._device) for k, v in inputs.items()}


        with torch.no_grad():
            audio_values = model.generate(
                **inputs, 
                do_sample=True,
                max_new_tokens=max_tokens,
                guidance_scale=3.0,
                streamer=BaseProgressStreamer(max_tokens, params.on_progress)
            )

        sampling_rate = model.config.audio_encoder.sampling_rate
        
        #if torch.cuda.is_available():
        data = audio_values.detach().to(torch.float32).clamp(-1, 1).cpu().numpy()
        #else:
            #data = audio_values[0, 0].numpy()

        scipy.io.wavfile.write(output_path, rate=sampling_rate, data=data)

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
