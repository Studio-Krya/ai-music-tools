# Krya AI Music Hub



## Instalando dependencias

1. Instalar o [uv](https://github.com/astral-sh/uv)
2. Instalar o `ffmpeg` na **versão 6** 


**Windows**

Installing on Windows

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

Text-to-Speech generation

[Github Repo](https://github.com/coqui-ai/TTS)

[Doc](https://github.com/coqui-ai/TTS?tab=readme-ov-file#command-line-tts)


**Comando Base**

```bash
uv run tts [...params]
```

**Modelos relevantes**

### AudioLDM

Generate speech, sound effects, music and beyond

[Github Repo](https://github.com/haoheliu/AudioLDM)

[Doc](https://github.com/haoheliu/AudioLDM?tab=readme-ov-file#commandline-usage)

**Comando Base**

```bash
uv run audioldm [...params]
```

**Modelos relevantes**


### Audiocraft
Library for audio processing and generation with deep learning

[Github Repo](https://github.com/facebookresearch/audiocraft)


**Comando Base**

```bash
uv run audio
```

**Modelos relevantes**

- `facebook/musicgen-small`: 300M model, text to music only - 🤗 Hub
- `facebook/musicgen-medium`: 1.5B model, text to music only - 🤗 Hub
- `facebook/musicgen-melody`: 1.5B model, text to music and text+melody to music - 🤗 Hub
- `facebook/musicgen-large`: 3.3B model, text to music only - 🤗 Hub
- `facebook/musicgen-melody-large`: 3.3B model, text to music and text+melody to music - 🤗 Hub
- `facebook/musicgen-stereo-*`: All the previous models fine tuned for stereo generation - small, medium, large, melody, melody large.



