#!/bin/bash

# Configura estos valores:
GITHUB_USER="GhostmanBY"
REPO="Shadow-Folder"
BASE_BRANCH="main"
TOKEN="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"  # Pon aquí tu token personal de GitHub
DATE_TAG=$(date +%Y%m%d%H%M%S)
DATE_HUMAN=$(date +%T)

cd /home/ghost/Escritorio/Repos/Shadow-Folder || exit 1

# Crear rama temporal
BRANCH="auto-pr-$DATE_TAG"
git checkout -b "$BRANCH"

# Agregar y commitear si hay cambios
git add .
if ! git diff --cached --quiet; then
  git commit -m "[auto] backup $DATE_HUMAN"

  # Hacer push (y abortar si falla)
  if ! git push origin "$BRANCH"; then
    echo "ERROR: Falló el push. Abortando."
    git checkout "$BASE_BRANCH"
    git branch -D "$BRANCH"
    exit 1
  fi

  # Crear Pull Request
  curl -X POST \
    -H "Authorization: token $TOKEN" \
    -H "Accept: application/vnd.github+json" \
    -d "{
      \"title\": \"Auto PR $DATE_TAG\",
      \"head\": \"$BRANCH\",
      \"base\": \"$BASE_BRANCH\",
      \"body\": \"Pull request automático cada 10 minutos.\"
    }" \
    "https://api.github.com/repos/$GITHUB_USER/$REPO/pulls"

else
  echo "No hay cambios para commitear."
  git checkout "$BASE_BRANCH"
  git branch -D "$BRANCH"
fi
