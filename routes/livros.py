from fastapi import APIRouter, HTTPException
from models import Livro
from utils.csv_manager import read_csv, write_csv

router = APIRouter()
FILEPATH = "data/livros.csv"

# Criar o arquivo CSV se não existir
@router.get("/", response_model=list[Livro])
def listar_livros():
    return [Livro(**livro) for livro in read_csv(FILEPATH)]

# Adicionar livro
@router.post("/", response_model=Livro)
def adicionar_livro(livro: Livro):
    livros = read_csv(FILEPATH)
    if any(int(l["id"]) == livro.id for l in livros):
        raise HTTPException(status_code=400, detail="ID já existe.")
    livros.append(livro.model_dump()) 
    write_csv(FILEPATH, livros)
    return livro

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
            return {"mensagem": "Livro deletado com sucesso"}
    raise HTTPException(status_code=404, detail="Livro não encontrado")
