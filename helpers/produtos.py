import requests
import uuid

from helpers.config import ENDPOINT


def criar_produto(token: str) -> str:
    """
    Cria um produto e retorna seu _id.
    Requer token de usuário administrador.
    """
    payload = {
        "nome": f"Produto {uuid.uuid4()}",
        "preco": 100,
        "descricao": "Produto de teste automatizado",
        "quantidade": 10
    }
    headers = {"Authorization": token}
    response = requests.post(f"{ENDPOINT}/produtos", json=payload, headers=headers)
    return response.json()["_id"]
