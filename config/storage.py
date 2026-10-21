from config.settings import SUPABASE_URL
import requests
import tempfile
import os

class Storage():
    def __init__(self, caminho):
        self.caminho = caminho

    def baixar_arquivo_temporario(self):

        url = SUPABASE_URL + self.caminho

        resposta = requests.get(url, timeout=30)
        resposta.raise_for_status()

        extensao = os.path.splitext(self.caminho)[1]

        arquivo = tempfile.NamedTemporaryFile(
            suffix=extensao,
            delete=False
        )

        try:
            arquivo.write(resposta.content)
        finally:
            arquivo.close()

        return arquivo.name

    