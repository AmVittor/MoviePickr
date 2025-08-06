import json
import os

FILMES_PATH = "dados/filmes.json"
ASSISTIDOS_PATH = "dados/assistidos.json"
NOTAS_PATH = "dados/notas.json"

def salvar_lista(caminho, lista):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)

def carregar_lista(caminho):
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_notas(caminho, dicionario):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dicionario, f, ensure_ascii=False, indent=2)

def carregar_notas(caminho):
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}
