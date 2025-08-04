#!/bin/bash

# Dosyaları sahnele
git add .

# Değişiklik varsa commit et
if ! git diff --cached --quiet; then
  git commit -m "Update site"
  git push
else
  echo "No changes to commit."
fi
