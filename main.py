# main.py
from fastapi import FastAPI
from routes import livros, usuarios, emprestimos

app = FastAPI(title="API Biblioteca Comunitária",
              description="Gerenciamento de livros usando FastAPI e CSV",
              version="1.0.0")

app.include_router(livros.router, prefix="/livros", tags=["Livros"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"])
app.include_router(emprestimos.router, prefix="/emprestimos", tags=["Empréstimos"])

@app.get("/")
def home():
    return {"mensagem": "Bem-vindo à API da Biblioteca Comunitária!"}
