from fastapi import FastAPI, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
import models

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ROTA PRINCIPAL: LISTAGEM
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    produtos = db.query(models.Produto).all()
    categorias = db.query(models.Categoria).all()
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "produtos": produtos, 
        "categorias": categorias
    })

# ROTA PARA CADASTRAR CATEGORIA
@app.post("/categoria/nova")
def cadastrar_categoria(nome: str = Form(...), descricao: str = Form(None), db: Session = Depends(get_db)):
    nova_cat = models.Categoria(nome=nome, descricao=descricao)
    db.add(nova_cat)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

# ROTA PARA CADASTRAR PRODUTO
@app.post("/produto/novo")
def cadastrar_produto(
    nome: str = Form(...), 
    preco: float = Form(...), 
    estoque: int = Form(...), 
    categoria_id: int = Form(...), 
    db: Session = Depends(get_db)
):
    novo_prod = models.Produto(nome=nome, preco=preco, estoque=estoque, categoria_id=categoria_id)
    db.add(novo_prod)
    db.commit()
    return RedirectResponse(url="/", status_code=303)