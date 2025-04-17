# models.py
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class Livro(BaseModel):
    id: int
    titulo: str
    autor: str
    genero: str
    ano_publicacao: int
    disponivel: bool = True

class Usuario(BaseModel):
    id: int
    nome: str
    email: EmailStr
    telefone: str
    data_cadastro: date

class Emprestimo(BaseModel):
    id: int
    livro_id: int
    usuario_id: int
    data_emprestimo: date
    data_devolucao: Optional[date] = None
    status: str  # "pendente" ou "devolvido"
