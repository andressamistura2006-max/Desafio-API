import requests
from jsonschema import validate

from helpers.config import ENDPOINT
from helpers.usuarios import gerar_email


# ==========================================
#  JSON SCHEMA — validacao de contrato
#
#  Garante que a estrutura das respostas
#  esta de acordo com o esperado, alem do
#  status code. Se a API remover ou mudar
#  o tipo de um campo, esses testes falham.
# ==========================================


# SCHEMA 1 — POST /usuarios (cadastro com sucesso)

SCHEMA_CADASTRO_USUARIO = {
    "type": "object",
    "required": ["message", "_id"],
    "properties": {
        "message": {"type": "string"},
        "_id":     {"type": "string"}
    },
    "additionalProperties": False
}

def test_schema_cadastrar_usuario():
    payload = {
        "nome": "Andressa Schema",
        "email": gerar_email(),
        "password": "123456",
        "administrador": "true"
    }
    response = requests.post(f"{ENDPOINT}/usuarios", json=payload)

    assert response.status_code == 201
    validate(instance=response.json(), schema=SCHEMA_CADASTRO_USUARIO)


# SCHEMA 2 — POST /login (reutiliza usuario_login da sessão)

SCHEMA_LOGIN = {
    "type": "object",
    "required": ["message", "authorization"],
    "properties": {
        "message":       {"type": "string"},
        "authorization": {"type": "string"}
    },
    "additionalProperties": False
}

def test_schema_login(usuario_login):
    email, password = usuario_login
    response = requests.post(
        f"{ENDPOINT}/login",
        json={"email": email, "password": password}
    )

    assert response.status_code == 200
    validate(instance=response.json(), schema=SCHEMA_LOGIN)


# SCHEMA 3 — GET /produtos (reutiliza produto_admin da sessão)

SCHEMA_PRODUTO_ITEM = {
    "type": "object",
    "required": ["nome", "preco", "descricao", "quantidade", "_id"],
    "properties": {
        "nome":       {"type": "string"},
        "preco":      {"type": "number"},
        "descricao":  {"type": "string"},
        "quantidade": {"type": "integer"},
        "_id":        {"type": "string"}
    }
}

SCHEMA_LISTAGEM_PRODUTOS = {
    "type": "object",
    "required": ["quantidade", "produtos"],
    "properties": {
        "quantidade": {"type": "integer"},
        "produtos": {
            "type": "array",
            "items": SCHEMA_PRODUTO_ITEM
        }
    }
}

def test_schema_listar_produtos():
    response = requests.get(f"{ENDPOINT}/produtos")

    assert response.status_code == 200
    validate(instance=response.json(), schema=SCHEMA_LISTAGEM_PRODUTOS)
