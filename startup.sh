#!/bin/bash
echo "Trying to update the project..."
git pull


install_alias_if_not_exists() {
    command_name=$1
    has_command=$(grep -q "^alias $command_name=" "$HOME/.bashrc" 2>/dev/null && echo "found" || echo "not found")

    if [ "$has_command" == "not found" ]; then
        echo "Alias $command_name not found, creating..."
        echo "alias $command_name='uv run $command_name'" >> ~/.bashrc
        
        # should create other bashrc files in the home directory if they don't exist
        if [ ! -f ~/.bash_profile ]; then
            touch ~/.bash_profile
        fi
    fi
}

install_alias_if_not_exists "krya"
install_alias_if_not_exists "tts"
install_alias_if_not_exists "audioldm"

# # check if the alias exists in the bashrc file even if the file doesnt exist
# has_command=$(grep -q '^alias krya=' "$HOME/.bashrc" 2>/dev/null && echo "found" || echo "not found")

# if [ "$has_command" == "not found" ]; then
#     echo "Alias krya not found, creating..."
#     echo "alias krya='uv run krya'" >> ~/.bashrc
    
#     # should create other bashrc files in the home directory if they don't exist
#     if [ ! -f ~/.bash_profile ]; then
#         touch ~/.bash_profile
#     fi
# fi
clear
