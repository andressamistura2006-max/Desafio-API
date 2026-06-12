import requests
import uuid

from helpers.config import ENDPOINT


def gerar_email():
    """Gera um e-mail único para evitar conflitos entre execuções."""
    return f"teste_{uuid.uuid4()}@email.com"


def criar_usuario():
    """Cria um usuário administrador e retorna seu _id."""
    payload = {
        "nome": "Usuario Teste",
        "email": gerar_email(),
        "password": "123456",
        "administrador": "true"
    }
    response = requests.post(f"{ENDPOINT}/usuarios", json=payload)
    return response.json()["_id"]
