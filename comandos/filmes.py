import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput, Select
import random
import requests
from dotenv import load_dotenv
import os

from dados.persistencia import (
    salvar_lista, carregar_lista,
    salvar_notas, carregar_notas,
    FILMES_PATH, ASSISTIDOS_PATH, NOTAS_PATH
)

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
filmes = carregar_lista(FILMES_PATH)
assistidos = carregar_lista(ASSISTIDOS_PATH)
notas_dict = carregar_notas(NOTAS_PATH)

def setup_filmes(bot):

    @bot.command(name="ajuda")
    async def lista_comandos(ctx):
        comandos = (
            "📜 **Comandos disponíveis:**\n"
            "`.addFilme [filmes separados por vírgula]` - Adiciona filmes à lista\n"
            "`.removerFilme` - Escolha um filme para ser removido da lista de filmes\n"
            "`.detalharFilme` - Escolha um filme para receber uma breve sinopse e poster\n"
            "`.listar` - Lista todos os filmes adicionados\n"
            "`.sortear` - Sorteia um filme aleatório\n"
            "`.avaliar` - Avalia um dos filmes assistidos\n"
            "`.mostrarNotas` - Mostra as notas dos filmes avaliados"
        )
        await ctx.reply(comandos)

    @bot.command()
    async def addFilme(ctx, *, lista_filmes: str):
        novos_filmes = [filme.strip() for filme in lista_filmes.split(",") if filme.strip()]
        if not novos_filmes:
            await ctx.reply("Nenhum filme válido fornecido.")
            return
        filmes.extend(novos_filmes)
        salvar_lista(FILMES_PATH, filmes)
        await ctx.reply(f"{len(novos_filmes)} filme(s) adicionados com sucesso!")

    @bot.command()
    async def removerFilme(ctx):
        if not filmes:
            await ctx.reply("Nenhum filme para remover.")
            return

        class ConfirmarRemocaoView(View):
            def __init__(self, filme):
                super().__init__(timeout=30)
                self.filme = filme

            @discord.ui.button(label="✅ Confirmar", style=discord.ButtonStyle.danger)
            async def confirmar(self, interaction: discord.Interaction, button: Button):
                if self.filme in filmes:
                    filmes.remove(self.filme)
                    salvar_lista(FILMES_PATH, filmes)
                    await interaction.response.edit_message(content=f"Filme **{self.filme}** removido com sucesso!", view=None)
                else:
                    await interaction.response.edit_message(content="Filme já não está na lista.", view=None)
                self.stop()

            @discord.ui.button(label="❌ Cancelar", style=discord.ButtonStyle.secondary)
            async def cancelar(self, interaction: discord.Interaction, button: Button):
                await interaction.response.edit_message(content="Remoção cancelada.", view=None)
                self.stop()

        class FilmeSelect(Select):
            def __init__(self):
                options = [
                    discord.SelectOption(label=filme, description=f"Remover {filme}")
                    for filme in filmes[:25]
                ]
                super().__init__(
                    placeholder="Escolha o filme para remover...",
                    min_values=1,
                    max_values=1,
                    options=options
                )

            async def callback(self, interaction: discord.Interaction):
                filme_selecionado = self.values[0]
                confirmar_view = ConfirmarRemocaoView(filme_selecionado)
                await interaction.response.edit_message(
                    content=f"Você quer realmente remover o filme **{filme_selecionado}**?",
                    view=confirmar_view
                )

        class CancelarView(View):
            def __init__(self, select: FilmeSelect):
                super().__init__(timeout=30)
                self.add_item(select)

            @discord.ui.button(label="❌ Cancelar", style=discord.ButtonStyle.secondary)
            async def cancelar(self, interaction: discord.Interaction, button: Button):
                await interaction.response.edit_message(content="Processo de remoção cancelado.", view=None)
                self.stop()

        select = FilmeSelect()
        cancelar_view = CancelarView(select)

        await ctx.reply("Selecione o filme que deseja remover ou cancele a operação:", view=cancelar_view)

    @bot.command(name="listar")
    async def listar_filmes(ctx):
        if not filmes:
            await ctx.reply("Nenhum filme foi adicionado ainda.")
            return
        lista = "\n".join(f"- {filme}" for filme in filmes)
        await ctx.reply(f"\U0001F3AC Lista de Filmes:\n{lista}")


    @bot.command()
    async def detalharFilme(ctx):
        if not filmes:
            await ctx.reply("Nenhum filme disponível para detalhar.")
            return

        class FilmeSelect(Select):
            def __init__(self):
                options = [
                    discord.SelectOption(label=filme, description=f"Detalhar {filme}")
                    for filme in filmes[:25]
                ]
                super().__init__(placeholder="Escolha o filme para ver detalhes", min_values=1, max_values=1, options=options)
                
            async def callback(self, interaction: discord.Interaction):
                filme_nome = self.values[0]
                url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={filme_nome}"
                resposta = requests.get(url).json()

                if resposta.get("Response") == "True":
                    titulo = resposta.get("Title", filme_nome)
                    sinopse = resposta.get("Plot", "Sem sinopse disponível.")
                    poster = resposta.get("Poster")

                    embed = discord.Embed(title=titulo, description=sinopse)
                    if poster and poster != "N/A":
                        embed.set_image(url=poster)

                    await interaction.response.edit_message(content=None, embed=embed, view=None)
                else:
                    await interaction.response.edit_message(content=f"Não encontrei detalhes para **{filme_nome}**.", view=None)

        class FilmeView(View):
            def __init__(self):
                super().__init__(timeout=60)
                self.add_item(FilmeSelect())

            @discord.ui.button(label="❌ Cancelar", style=discord.ButtonStyle.secondary)
            async def cancelar(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.edit_message(content="Detalhar o filme cancelado", view=None)
                self.stop()
                    

        await ctx.reply("Escolha o filme para ver detalhes:", view=FilmeView())

    @bot.command()
    async def sortear(ctx):
        if not filmes:
            await ctx.reply("A lista de filmes está vazia")
            return

        class ConfirmarView(View):
            def __init__(self, filme):
                super().__init__(timeout=60)
                self.filme = filme

            @discord.ui.button(label="✅ Sim", style=discord.ButtonStyle.success)
            async def confirmar(self, interaction: discord.Interaction, button: Button):
                assistidos.append(self.filme)
                filmes.remove(self.filme)
                salvar_lista(FILMES_PATH, filmes)
                salvar_lista(ASSISTIDOS_PATH, assistidos)
                await interaction.response.edit_message(content=f"Filme **{self.filme}** adicionado aos assistidos! ✅", view=None)
                self.stop()

            @discord.ui.button(label="❌ Não", style=discord.ButtonStyle.danger)
            async def negar(self, interaction: discord.Interaction, button: Button):
                if not filmes:
                    await interaction.response.edit_message(content="Nenhum outro filme para sortear.", view=None)
                    self.stop()
                    return
                novo_filme = random.choice(filmes)
                self.filme = novo_filme
                await interaction.response.edit_message(content=f"Filme sorteado: **{novo_filme}**\nFilme decidido?", view=self)

        filme_sorteado = random.choice(filmes)
        await ctx.send(f"Filme sorteado: **{filme_sorteado}**\nFilme decidido?", view=ConfirmarView(filme_sorteado))

    @bot.command()
    async def avaliar(ctx):
        if not assistidos:
            await ctx.reply("Nenhum filme assistido para avaliar.")
            return

        class FilmeButton(Button):
            def __init__(self, filme):
                super().__init__(label=filme, style=discord.ButtonStyle.primary)
                self.filme = filme

            async def callback(self, interaction: discord.Interaction):
                await interaction.response.send_modal(AvaliarModal(self.filme))

        class AvaliarView(View):
            def __init__(self):
                super().__init__(timeout=60)
                for filme in assistidos[:5]:
                    self.add_item(FilmeButton(filme))

        class AvaliarModal(Modal):
            def __init__(self, filme):
                super().__init__(title=f"Avaliar: {filme}")
                self.filme = filme
                self.nota_input = TextInput(label="Digite a nota (0 a 10)", placeholder="Ex: 8.5")
                self.add_item(self.nota_input)

            async def on_submit(self, interaction: discord.Interaction):
                try:
                    nota = float(self.nota_input.value)
                    if not 0 <= nota <= 10:
                        raise ValueError()
                    notas_dict[self.filme] = nota
                    salvar_notas(NOTAS_PATH, notas_dict)
                    await interaction.response.send_message(f"✅ Nota {nota} registrada para **{self.filme}**", ephemeral=True)
                except ValueError:
                    await interaction.response.send_message("\u274C Nota inválida. Use um número entre 0 e 10.", ephemeral=True)

        await ctx.send("Escolha um filme para avaliar:", view=AvaliarView())

    @bot.command(name="mostrarNotas")
    async def mostrar_notas(ctx):
        if not notas_dict:
            await ctx.reply("Nenhuma nota foi registrada ainda.")
            return
        mensagem = "\U0001F3AC Notas dos filmes:\n"
        for filme, nota in notas_dict.items():
            mensagem += f"- **{filme}**: {nota}\n"
        await ctx.reply(mensagem)
