#!/bin/bash

USER=$USERNAME

TTS_DIR="/d/models/.local/share/tts/."
CACHE_DIR="/d/models/.cache/."

CACHE_DIR_OUT="/c/Users/$USER/.cache/"
TTS_DIR_OUT="/c/Users/$USER/AppData/Local/tts"

echo "Pulling latest changes from git"
git pull

echo "Copying models from $FROM to $TO"

cp -r $TTS_DIR $TTS_DIR_OUT
cp -r $CACHE_DIR $CACHE_DIR_OUT

# copying the shortcut to the desktop
cp "./Krya AI Tools.lnk" "/c/Users/$USER/Desktop/Krya AI Tools.lnk"