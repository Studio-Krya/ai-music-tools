@echo off
set "TARGET_DIR=C:\Users\%USERNAME%\ai-music-tools"

start "Krya AI Music Tools" "C:\Program Files\Git\git-bash.exe" --cd="%TARGET_DIR%" -c "bash ./startup.sh; exec bash"

