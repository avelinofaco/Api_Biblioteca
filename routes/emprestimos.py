from fastapi import APIRouter, HTTPException, Query
from models import Emprestimo
from utils.csv_manager import read_csv, write_csv
from routes.usuarios import FILEPATH as USUARIOS_FILE
from routes.livros import FILEPATH as LIVROS_FILE

from fastapi.responses import FileResponse
import zipfile
import os

router = APIRouter()
FILEPATH = "data/emprestimos.csv"

#Listar empréstimos com filtros
# Criar o arquivo CSV se não existir
@router.get("/", response_model=list[Emprestimo])
def listar_emprestimos(
    usuario_id: int = Query(default=None),
    livro_id: int = Query(default=None),
    data_emprestimo: str = Query(default=None),  # formato: YYYY-MM-DD
    data_devolucao: str = Query(default=None),   # formato: YYYY-MM-DD
):
    emprestimos = [Emprestimo(**e) for e in read_csv(FILEPATH)]

    if usuario_id is not None:
        emprestimos = [e for e in emprestimos if e.usuario_id == usuario_id]
    if livro_id is not None:
        emprestimos = [e for e in emprestimos if e.livro_id == livro_id]
    if data_emprestimo:
        emprestimos = [e for e in emprestimos if str(e.data_emprestimo) == data_emprestimo]
    if data_devolucao:
        emprestimos = [e for e in emprestimos if str(e.data_devolucao) == data_devolucao]

    return emprestimos

# Obter a quantidade de empréstimos
@router.get("/quantidade")
def quantidade_emprestimos():
    emprestimos = read_csv(FILEPATH)
    return {"quantidade": len(emprestimos)}

# Exportar empréstimos para ZIP
@router.get("/exportar")
def exportar_emprestimos():
    zip_path = "data/emprestimos.zip"
    csv_path = "data/emprestimos.csv"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_path, arcname="emprestimos.csv")

    return FileResponse(zip_path, media_type="application/zip", filename="emprestimos.zip")

# Obter um empréstimo específico
@router.get("/{id}", response_model=Emprestimo)
def obter_emprestimo(id: int):
    emprestimos = read_csv(FILEPATH)
    for e in emprestimos:
        if int(e["id"]) == id:
            return Emprestimo(**e)
    raise HTTPException(status_code=404, detail="Empréstimo não encontrado.")

# Criar um novo empréstimo
@router.post("/", response_model=Emprestimo)
def adicionar_emprestimo(emprestimo: Emprestimo):
    emprestimos = read_csv(FILEPATH)
    livros = read_csv(LIVROS_FILE)
    usuarios = read_csv(USUARIOS_FILE)
    
    # Verifica se usuário existe
    if not any(int(u["id"]) == emprestimo.usuario_id for u in usuarios):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Verifica se livro existe
    livro = next((l for l in livros if int(l["id"]) == emprestimo.livro_id), None)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    # Verifica se o livro está disponível
    if livro.get("disponivel", "True") == "False":
        raise HTTPException(status_code=400, detail="Livro não está disponível para empréstimo")

    # Marca livro como indisponível (se desejar fazer isso aqui)
    livro["disponivel"] = False
    write_csv(LIVROS_FILE, livros)

    emprestimos.append(emprestimo.model_dump())
    write_csv(FILEPATH, emprestimos)
    return emprestimo

# Atualizar um empréstimo existente
@router.put("/{id}", response_model=Emprestimo)
def atualizar_emprestimo(id: int, dados: Emprestimo):
    emprestimos = read_csv(FILEPATH)
    for i, e in enumerate(emprestimos):
        if int(e["id"]) == id:
            emprestimos[i] = dados.model_dump()
            write_csv(FILEPATH, emprestimos)
            return dados
    raise HTTPException(status_code=404, detail="Empréstimo não encontrado.")

# Deletar um empréstimo
@router.delete("/{id}")
def deletar_emprestimo(id: int):
    emprestimos = read_csv(FILEPATH)
    novos = [e for e in emprestimos if int(e["id"]) != id]
    if len(novos) == len(emprestimos):
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado.")
    write_csv(FILEPATH, novos)
    return {"detail": "Empréstimo excluído com sucesso."}
