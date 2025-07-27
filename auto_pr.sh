#!/bin/bash

# Configura estos valores:
GITHUB_USER="GhostmanBY"
REPO="Shadow-Folder"
BASE_BRANCH="main"
TOKEN="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"  # Pon aquí tu token personal de GitHub

cd /home/ghost/Escritorio/Repos/Shadow-Folder

# Crea una rama única por fecha/hora
BRANCH="auto-pr-$(date +%Y%m%d%H%M%S)"
git checkout -b "$BRANCH"

# Añade y commitea cambios si los hay
git add .
if ! git diff --cached --quiet; then
  git commit -m "[auto] backup $(date +%T)"
  git push origin "$BRANCH"

  # Crea el pull request vía API
  curl -X POST -H "Authorization: token $TOKEN" \
    -d "{\"title\":\"Auto PR $(date)\",\"head\":\"$BRANCH\",\"base\":\"$BASE_BRANCH\",\"body\":\"Pull request automático cada 10 minutos\"}" \
    "https://api.github.com/repos/$GITHUB_USER/$REPO/pulls"
else
  echo "No hay cambios para commitear."
  git checkout "$BASE_BRANCH"
  git branch -D "$BRANCH"
fi