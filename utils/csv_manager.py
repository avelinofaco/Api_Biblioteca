import csv
from typing import List, Dict # Importando List e Dict para tipagem de dados

def read_csv(filepath: str) -> List[Dict]: # Ler o arquivo CSV e retornar uma lista de dicionários
    try:
        with open(filepath, mode="r", newline="", encoding="utf-8") as file: # Abrindo o arquivo CSV
            reader = csv.DictReader(file) # Criando um leitor de dicionários
            return list(reader) # Retornando a lista de dicionários
    except FileNotFoundError: # Se o arquivo não for encontrado, retornar uma lista vazia
        return [] 

def write_csv(filepath: str, data: List[Dict]): # Escrever os dados no arquivo CSV
    if not data: # Se os dados estiverem vazios, não fazer nada
        return
    with open(filepath, mode="w", newline="", encoding="utf-8") as file: # Abrindo o arquivo CSV para escrita
        writer = csv.DictWriter(file, fieldnames=data[0].keys()) # Criando um escritor de dicionários
        writer.writeheader() # Escrevendo o cabeçalho no arquivo CSV
        writer.writerows(data) # Escrevendo os dados no arquivo CSV
