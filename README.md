# 🎬 MoviePickr Bot

Um bot para Discord que sorteia filmes, registra avaliações e gerencia sua lista de filmes assistidos e por assistir. Ideal para grupos de amigos ou comunidades que gostam de cinema!

## 🚀 Funcionalidades

- 📥 **Adicionar filmes** à lista
- 📋 **Listar todos os filmes** disponíveis para assistir
- 🎲 **Sortear um filme aleatório**
- ✅ **Confirmar ou recusar** o filme sorteado
- 🎯 **Registrar nota** para os filmes assistidos
- ⭐ **Visualizar notas** dos filmes já avaliados

## 🧠 Como funciona

- Filmes são armazenados em arquivos `.json` para persistência.
- O bot mantém três listas:
  - `filmes.json`: filmes ainda não assistidos
  - `assistidos.json`: filmes que já foram assistidos
  - `notas.json`: notas dos filmes avaliados

## 💻 Comandos disponíveis

| Comando                | Descrição                                                 |
|------------------------|-----------------------------------------------------------|
| `.addFilme nome1, nome2` | Adiciona um ou mais filmes à lista (separados por vírgula) |
| `.listar`              | Lista todos os filmes ainda não assistidos               |
| `.sortear`             | Sorteia um filme aleatoriamente                          |
| `.avaliar`             | Permite avaliar filmes da lista de assistidos            |
| `.mostrarNotas`        | Mostra as notas dos filmes já avaliados                  |
| `.ajuda`               | Lista todos os comandos disponíveis                       |

> ⚠️ O comando `.help` foi renomeado para `.ajuda` para evitar conflitos com o comando interno do Discord.py.

## 🛠 Requisitos

- Python 3.10+
- Bibliotecas:
  - discord.py (v2+)

Instale os requisitos com:

```bash
pip install -r requirements.txt


