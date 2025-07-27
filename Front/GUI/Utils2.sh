#!/bin/bash

# Diccionario: tipo MIME => archivo .desktop
declare -A asociaciones=(
  ["text/plain"]="code.desktop"
  ["application/pdf"]="org.pwmt.zathura.desktop"
  ["image/png"]="feh.desktop"
  ["audio/mpeg"]="vlc.desktop"
  ["video/mp4"]="vlc.desktop"
)

for tipo in "${!asociaciones[@]}"; do
  app="${asociaciones[$tipo]}"
  echo "Asignando $app para $tipo"
  xdg-mime default "$app" "$tipo"
done
