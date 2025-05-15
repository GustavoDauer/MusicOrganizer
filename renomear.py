import os
import re
from mutagen import File

# Extensões de arquivos de áudio suportadas
audio_extensions = ['.mp3', '.flac', '.wav', '.m4a', '.ogg', '.aac']

def limpar_nome(nome):
    """Remove caracteres inválidos para nomes de arquivos sem alterar o case."""
    if nome:
        nome = re.sub(r'[\\/:"*?<>|]+', '', nome)
        nome = nome.strip().replace('\n', '').replace('\r', '')
    return nome

def obter_metadados(caminho_arquivo):
    try:
        audio = File(caminho_arquivo, easy=True)
        if not audio:
            return None, None
        artista = audio.get('artist', [None])[0]
        titulo = audio.get('title', [None])[0]

        return limpar_nome(artista), limpar_nome(titulo)
    except Exception as e:
        print(f"Erro ao ler metadados de {caminho_arquivo}: {e}")
        return None, None

def gerar_nome_unico(pasta, base_nome, extensao):
    """Gera um nome único caso o arquivo já exista."""
    contador = 1
    novo_nome = f"{base_nome}{extensao}"
    novo_caminho = os.path.join(pasta, novo_nome)

    while os.path.exists(novo_caminho):
        novo_nome = f"{base_nome} ({contador}){extensao}"
        novo_caminho = os.path.join(pasta, novo_nome)
        contador += 1

    return novo_nome

def renomear_arquivos_audio(pasta_raiz):
    for arquivo in os.listdir(pasta_raiz):
        caminho_completo = os.path.join(pasta_raiz, arquivo)

        if os.path.isfile(caminho_completo):
            _, extensao = os.path.splitext(arquivo)

            if extensao.lower() in audio_extensions:
                artista, titulo = obter_metadados(caminho_completo)

                if artista and titulo:
                    base_nome = f"{artista} - {titulo}"
                    base_nome = limpar_nome(base_nome)
                    novo_nome = gerar_nome_unico(pasta_raiz, base_nome, extensao)
                    novo_caminho = os.path.join(pasta_raiz, novo_nome)

                    try:
                        os.rename(caminho_completo, novo_caminho)
                        print(f"Renomeado: {arquivo} → {novo_nome}")
                    except Exception as e:
                        print(f"Erro ao renomear {arquivo}: {e}")
                else:
                    print(f"Metadados ausentes em: {arquivo}")

if __name__ == "__main__":
    pasta_atual = os.getcwd()
    renomear_arquivos_audio(pasta_atual)

