#!/bin/bash

USER=$USERNAME
FROM="/d/models/"
TO="/c/Users/$USER"

echo "Pulling latest changes from git"
git pull

echo "Copying models from $FROM to $TO"

cp -r $FROM $TO

# copying the shortcut to the desktop
cp "./Krya AI Tools.lnk" "/c/Users/$USER/Desktop/Krya AI Tools.lnk"