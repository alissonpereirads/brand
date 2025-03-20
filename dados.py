import pandas as pd
import os


def get_excel(path: str = ""):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo {path} não encontrado")

    try:
        data = pd.read_excel(path)
        print(f"Base de dados carregada com {len(data)} entradas.")  # Verificação
        return data
    except Exception as e:
        raise Exception(f"Erro ao ler o arquivo Excel: {e}")
