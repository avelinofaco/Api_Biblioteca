# main.py
from fastapi import FastAPI
from routes import livros

app = FastAPI(title="API Biblioteca Comunitária",
              description="Gerenciamento de livros usando FastAPI e CSV",
              version="1.0.0")

app.include_router(livros.router, prefix="/livros", tags=["Livros"])

@app.get("/")
def home():
    return {"mensagem": "Bem-vindo à API da Biblioteca Comunitária!"}
