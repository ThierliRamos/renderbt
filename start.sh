#!/bin/bash

# Detectar a versão do Python
if command -v python3 &>/dev/null; then
    exec python3 app.py
elif command -v python &>/dev/null; then
    exec python app.py
else
    echo "Python não está instalado"
    exit 1
fi