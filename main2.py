from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv
import os

app = FastAPI()

CSV_FILE = "database.csv"

class Produto(BaseModel):
    id: int
    nome: str
    preco: float
    quantidade: int

def ler_csv():
    produtos = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                produtos.append(Produto(
                    id= int(row["id"]),
                    nome= row["nome"],
                    preco= float(row["preco"]),
                    quantidade= int(row["quantidade"])
                ))
    return produtos

def escrever_csv(produtos):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["id", "nome", "preco", "quantidade"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for produto in produtos:
            writer.writerow(produto.dict())

@app.get("/produtos", response_model=list[Produto])
def listar_produtos():
    return ler_csv()

def buscar_id_csv(produto_id: int):
    produtos = ler_csv()
    for p in produtos:
        if p.id == produto_id:
            return p
    return None

@app.post("/produtos", response_model=Produto)
def criar_produto(produto: Produto):
    produtos = ler_csv()
    if any(p.id == produto.id for p in produtos):
        raise HTTPException(status_code=400, detail="Id já existe")
    produtos.append(produto)
    escrever_csv(produtos)
    return produto

@app.get("/produtos/{produto_id}", response_model=Produto)
def buscar_por_id(produto_id : int):
    produto = buscar_id_csv(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não econtrado")
    return produto

@app.put("/produtos/{produto_id}", response_model=Produto)


@app.delete("/produtos/{id_produto}", response_model=dict)
def deletar_produtor(produto_id: int):
    produtos = listar_produtos()

    produtos_filtrados = [produto for produto in produtos if produto.id != produto_id]
    if len(produtos) == len(produtos_filtrados):
        raise HTTPException(404, detail="produto não encontrado")

    escrever_csv(produtos_filtrados)
    return {"msg": "produto deletado com sucesso"}