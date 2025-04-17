from fastapi import APIRouter, HTTPException
from models import Usuario
from utils.csv_manager import read_csv, write_csv

router = APIRouter()
FILEPATH = "data/usuarios.csv"

# Listar todos os usuários
@router.get("/", response_model=list[Usuario])
def listar_usuarios():
    return [Usuario(**usuario) for usuario in read_csv(FILEPATH)]

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
