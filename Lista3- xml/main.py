from fastapi import FastAPI, HTTPException
from typing import List
from models import Livro
from xml_utils import carregar_livros, salvar_livros, buscar_livro_por_id

app = FastAPI()

# Busca todos os livros
@app.get("/livros", response_model=List[Livro])
def listar_livros():
    return carregar_livros()

# Busca um livro pelo ID
@app.get("/livros/{livro_id}", response_model=Livro)
def obter_livro(livro_id: int): 
    livro = buscar_livro_por_id(livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro

#Adiciona um novo livro
@app.post("/livros", response_model=Livro)
def adicionar_livro(livro: Livro):
    livros = carregar_livros()
    if any(l.id == livro.id for l in livros):
        raise HTTPException(status_code=400, detail="ID já existente")
    livros.append(livro)
    salvar_livros(livros)
    return livro

#Atualiza um livro existente
@app.put("/livros/{livro_id}", response_model=Livro)
def atualizar_livro(livro_id: int, livro_atualizado: Livro):
    livros = carregar_livros()
    for i, l in enumerate(livros):
        if l.id == livro_id:
            livros[i] = livro_atualizado
            salvar_livros(livros)
            return livro_atualizado
    raise HTTPException(status_code=404, detail="Livro não encontrado")

#Deleta um livro existente
@app.delete("/livros/{livro_id}")
def deletar_livro(livro_id: int):
    livros = carregar_livros()
    livros_filtrados = [l for l in livros if l.id != livro_id]
    if len(livros) == len(livros_filtrados):
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    salvar_livros(livros_filtrados)
    return {"mensagem": "Livro deletado com sucesso"}
