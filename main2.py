from fastapi import FastAPI
from pydantic import Basemodel
import csv
import os

app = FastAPI()

CSV_FILE = "database.csv"

class Produto(Basemodel):
    id: int
    nome: str
    preco: float
    quantidade: int

def ler_csv():
    produtos = []
    if os.path.exists(CSV_FILE)
        with open(CSV_FILE, mode="r", newline="", enconding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                produtos.append(Produto(**row))
    return produtos

def escrever_csv(produtos):
    with open(CSV_FILE, mode="r", newline="", enconding="utf-8") as file:
        fieldnames = ["id", "nome", "preco", "quantidade"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerheader()
        for produto in produtos:
            writer.writerow(produto.dict())