from fastapi import FastAPI, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
import models

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request:Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"request":request}
    )

@app.post("/categoria/nova")
def criar_categoria(nome: str = Form(...), descricao: str = Form(None), db: Session = Depends(get_db)):
    nova_cat = models.Categoria(nome=nome, descricao=descricao)
    db.add(nova_cat)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/produto/novo")
def criar_produto(
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