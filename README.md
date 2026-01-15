# Krya AI Music Hub



## Instalando dependencias

1. Instalar o [uv](https://github.com/astral-sh/uv)
2. Instalar o `ffmpeg` na **versão 6** 


**Windows**

Instalando no Windows

```powershell
# Install uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install ffmpeg
winget install --id=Gyan.FFmpeg --version 6.1.1 -e
``` 

Após concluir a instalação de ambos, rode o comando dentro da pasta do projeto

```bash
uv sync
```


**Para executar os comandos no terminal, é preciso incluir `uv run` antes deles**

```bash
uv run tts --model_info_by_name tts_models/pt/cv/vits
```

## Modelos

### CoquiTTS

[Github Repo](https://github.com/coqui-ai/TTS)

🐸TTS is a library for advanced Text-to-Speech generation.

🚀 Pretrained models in +1100 languages.

🛠️ Tools for training new models and fine-tuning existing models in any language.

📚 Utilities for dataset analysis and curation.




#### Comandos
[Documentação](https://github.com/coqui-ai/TTS?tab=readme-ov-file#command-line-tts)

**Comando Base**

```bash
uv run tts [...params]
```

**Lista os modelos**

```bash
uv run tts --list_models
```


### AudioLDM

[Github Repo](https://github.com/haoheliu/AudioLDM)

Generate speech, sound effects, music and beyond.

- Text-to-Audio Generation: Generate audio given text input.
- Audio-to-Audio Generation: Given an audio, generate another audio that contain the same type of sound.
- Text-guided Audio-to-Audio Style Transfer: Transfer the sound of an audio into another one using the text description.



#### Comandos

[Documentação](https://github.com/haoheliu/AudioLDM?tab=readme-ov-file#commandline-usage)

**Comando base**

```bash
uv run audioldm [...params]
```

#### Modelos relevantes

- `audioldm-s-full`
- `audioldm-m-full`


### Audiocraft

[Github Repo](https://github.com/facebookresearch/audiocraft)

AudioCraft is a PyTorch library for deep learning research on audio generation. AudioCraft contains inference and training code for two state-of-the-art AI generative models producing high-quality audio: AudioGen and MusicGen.



#### Comandos

**Cria uma melodia através de um prompt**

```sh
uv run krya audiocraft musicgen [-o,--output] {nome}.wav [-m,--model] {modelo} [-d,--duration] {duracao_segundos} "Sua prompt" 
```

exemplo

```sh
uv run krya audiocraft musicgen --output demo.wav -m facebook/musicgen-medium -d 10 "A vibe lo-fi in desert"
```

#### Modelos relevantes

- `facebook/musicgen-small`: 300M model, text to music only - 🤗 Hub
- `facebook/musicgen-medium`: 1.5B model, text to music only - 🤗 Hub
- `facebook/musicgen-melody`: 1.5B model, text to music and text+melody to music - 🤗 Hub
- `facebook/musicgen-large`: 3.3B model, text to music only - 🤗 Hub
- `facebook/musicgen-melody-large`: 3.3B model, text to music and text+melody to music - 🤗 Hub
- `facebook/musicgen-stereo-*`: All the previous models fine tuned for stereo generation - small, medium, large, melody, melody large.



