# Krya AI Music Hub



## Instalando dependencias

1. Instalar o [uv](https://github.com/astral-sh/uv) na máquina
2. Instalar o [ffmpeg v6](https://www.ffmpeg.org/download.html) na máquina

**Windows**

Installing on Windows

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
winget install --id=Gyan.FFmpeg --version 6.1.1 -e
``` 

Após concluir a instalação de ambos, rode o comando dentro da pasta do projeto

```
uv sync
```


## Bibliotecas

Modelo | Descrição | Comando no Terminal | Link do repositório
------ | --------- | ------------------- | --
CoquiTTS | Text-to-Speech generation | `uv run tts` | https://github.com/coqui-ai/TTS
AudioLDM | Generate speech, sound effects, music and beyond | `uv run audildm` | https://github.com/haoheliu/AudioLDM
Audiocraft | Library for audio processing and generation with deep learning | `uv run dora` | https://github.com/facebookresearch/audiocraft



**Para executar os comandos no terminal, é preciso incluir `uv run` antes deles**

```
uv run tts --model_info_by_name tts_models/tr/common-voice/glow-tts
```

## Modelos

### Audiocraft

[Github Repo](https://github.com/facebookresearch/audiocraft)

Library for audio processing and generation with deep learning

```
```

- `facebook/musicgen-small`: 300M model, text to music only - 🤗 Hub
- `facebook/musicgen-medium`: 1.5B model, text to music only - 🤗 Hub
- `facebook/musicgen-melody`: 1.5B model, text to music and text+melody to music - 🤗 Hub
- `facebook/musicgen-large`: 3.3B model, text to music only - 🤗 Hub
- `facebook/musicgen-melody-large`: 3.3B model, text to music and text+melody to music - 🤗 Hub
- `facebook/musicgen-stereo-*`: All the previous models fine tuned for stereo generation - small, medium, large, melody, melody large.



