from fastapi import APIRouter, HTTPException, Query
from models import Usuario
from utils.csv_manager import read_csv, write_csv

import zipfile
import os 
from fastapi.responses import FileResponse

router = APIRouter()
FILEPATH = "data/usuarios.csv"

# Listar usuários com filtros
@router.get("/", response_model=list[Usuario])
def listar_usuarios(
    nome: str = Query(default=None),
    email: str = Query(default=None),
    telefone: str = Query(default=None),
    data_cadastro: str = Query(default=None),  # formato: YYYY-MM-DD
):
    usuarios = [Usuario(**u) for u in read_csv(FILEPATH)]

    if nome:
        usuarios = [u for u in usuarios if nome.lower() in u.nome.lower()]
    if email:
        usuarios = [u for u in usuarios if email.lower() in u.email.lower()]
    if telefone:
        usuarios = [u for u in usuarios if telefone in u.telefone]
    if data_cadastro:
        usuarios = [u for u in usuarios if str(u.data_cadastro) == data_cadastro]

    return usuarios


# Contar usuários
@router.get("/quantidade", response_model=dict)
def contar_usuarios():
    usuarios = read_csv(FILEPATH)
    return {"quantidade": len(usuarios)}

# Exportar usuários para ZIP
@router.get("/exportar")
def exportar_usuarios():
    zip_filename = "usuarios.zip"
    csv_filename = FILEPATH

    # Cria o ZIP com o CSV dentro
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        zipf.write(csv_filename, arcname="usuarios.csv")

    # Retorna o ZIP como download
    return FileResponse(path=zip_filename, filename=zip_filename, media_type="application/zip")


# Obter usuário por ID
@router.get("/{usuario_id}", response_model=Usuario)
def obter_usuario(usuario_id: int):
    usuarios = read_csv(FILEPATH)
    for usuario in usuarios:
        if int(usuario["id"]) == usuario_id:
            return Usuario(**usuario)
    raise HTTPException(status_code=404, detail="Usuário não encontrado.")

# Adicionar novo usuário
@router.post("/", response_model=Usuario)
def adicionar_usuario(usuario: Usuario):
    usuarios = read_csv(FILEPATH)
    if any(int(u["id"]) == usuario.id for u in usuarios):
        raise HTTPException(status_code=400, detail="ID já existe.")
    usuarios.append(usuario.model_dump())
    write_csv(FILEPATH, usuarios)
    return usuario

# Atualizar usuário
@router.put("/{usuario_id}", response_model=Usuario)
def atualizar_usuario(usuario_id: int, usuario_atualizado: Usuario):
    usuarios = read_csv(FILEPATH)
    for index, usuario in enumerate(usuarios):
        if int(usuario["id"]) == usuario_id:
            usuarios[index] = usuario_atualizado.model_dump()
            write_csv(FILEPATH, usuarios) 
            return usuario_atualizado
    raise HTTPException(status_code=404, detail="Usuário não encontrado.")

# Deletar usuário
@router.delete("/{usuario_id}")
def deletar_usuario(usuario_id: int):
    usuarios = read_csv(FILEPATH)
    for index, usuario in enumerate(usuarios):
        if int(usuario["id"]) == usuario_id:
            del usuarios[index]
            write_csv(FILEPATH, usuarios)
            return {"mensagem": "Usuário deletado com sucesso"}
    raise HTTPException(status_code=404, detail="Usuário não encontrado.")

