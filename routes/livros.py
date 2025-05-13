from fastapi import APIRouter, HTTPException, Query
from models import Livro
from utils.csv_manager import read_csv, write_csv
from hashlib import sha256
from typing import List
from utils.logger import logger
from fastapi.responses import FileResponse
import zipfile
from utils.xml import csv_xml

router = APIRouter()
FILEPATH = "data/livros.csv"

# Criar o arquivo CSV se não existir

@router.get("/", response_model=List[Livro])
def listar_livros(
    autor: str = Query(default=None),
    genero: str = Query(default=None),
    ano_publicacao: int = Query(default=None),
):
    livros = [Livro(**l) for l in read_csv(FILEPATH)]

    if autor:
        livros = [l for l in livros if l.autor.lower() == autor.lower()]
    if genero:
        livros = [l for l in livros if l.genero.lower() == genero.lower()]
    if ano_publicacao:
        livros = [l for l in livros if l.ano_publicacao == ano_publicacao]

    return livros

# Contar livros
@router.get("/quantidade", response_model=dict)
def contar_livros():
    livros = read_csv(FILEPATH)
    return {"quantidade": len(livros)}

# Exportar livros para ZIP
@router.get("/exportar")
def exportar_livros():
    zip_path = "data/livros.zip"
    csv_path = "data/livros.csv"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_path, arcname="livros.csv")

    return FileResponse(zip_path, media_type="application/zip", filename="livros.zip")

# Adicionar livro
@router.post("/", response_model=Livro)
def adicionar_livro(livro: Livro):
    livros = read_csv(FILEPATH)
    if any(int(l["id"]) == livro.id for l in livros):
        raise HTTPException(status_code=400, detail="ID já existe.")
    livros.append(livro.model_dump())
    write_csv(FILEPATH, livros)
    logger.info(f"Livro Criado: {livro}")
    return livro

# Hash do livro no zip
@router.get("/hash")
def hash_csv():
    with open("data/livros.zip", "rb") as stream:
        hash = sha256(stream.read()).hexdigest()
        return {"hash": hash}

# Buscar livro por ID
@router.get("/{id}", response_model=Livro)
def buscar_livro(id: int):
    livros = read_csv(FILEPATH)
    for livro in livros:
        if int(livro["id"]) == id:
            return Livro(**livro)
    raise HTTPException(status_code=404, detail="Livro não encontrado")

# Atualizar livro
@router.put("/{id}", response_model=Livro)
def atualizar_livro(id: int, livro_atualizado: Livro):
    livros = read_csv(FILEPATH)
    for i, livro in enumerate(livros):
        if int(livro["id"]) == id:
            livros[i] = livro_atualizado.model_dump()  # <- aqui também
            write_csv(FILEPATH, livros)
            logger.info(f"Livro Atualizado: {livro}")
            return livro_atualizado
    raise HTTPException(status_code=404, detail="Livro não encontrado")

# Deletar livro
@router.delete("/{id}")
def deletar_livro(id: int):
    livros = read_csv(FILEPATH)
    for i, livro in enumerate(livros):
        if int(livro["id"]) == id:
            del livros[i]
            write_csv(FILEPATH, livros)
            logger.info(f"Livro Deletado: {livro}")
            return {"mensagem": "Livro deletado com sucesso"}
    raise HTTPException(status_code=404, detail="Livro não encontrado")

#CSV para XML
@router.get("/csv-para-xml/{nome_csv}")
def escrever_dados_xml_de_csv():
    
    nome_base = "livros"
    caminho_csv = f"data/{nome_base}.csv"
    caminho_xml = f"data/{nome_base}.xml"

    csv_xml(caminho_csv, nome_base, caminho_xml)
    logger.info(f"Arquivo {nome_base}.csv convertido para XML")
    
    return FileResponse(path=caminho_xml, filename=f"{nome_base}.xml", media_type="application/xml")