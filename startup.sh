#!/bin/bash
echo "Trying to update the project..."
git pull

# check if the alias exists in the bashrc file even if the file doesnt exist
has_command=$(grep -q '^alias krya=' "$HOME/.bashrc" 2>/dev/null && echo "found" || echo "not found")

if [ "$has_command" == "not found" ]; then
    echo "Alias krya not found, creating..."
    echo "alias krya='uv run krya'" >> ~/.bashrc
    
    # should create other bashrc files in the home directory if they don't exist
    if [ ! -f ~/.bash_profile ]; then
        touch ~/.bash_profile
    fi
fi