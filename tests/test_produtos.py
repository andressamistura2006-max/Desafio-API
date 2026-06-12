import requests
import uuid

from helpers.config import ENDPOINT
from helpers.produtos import criar_produto


# LISTAR PRODUTOS

def test_listar_produtos():
    response = requests.get(f"{ENDPOINT}/produtos")

    assert response.status_code == 200
    assert "produtos" in response.json()


# BUSCAR PRODUTO POR ID

def test_buscar_produto_por_id():
    response = requests.get(f"{ENDPOINT}/produtos")
    produto_id = response.json()["produtos"][0]["_id"]

    busca = requests.get(f"{ENDPOINT}/produtos/{produto_id}")

    assert busca.status_code == 200
    assert busca.json()["_id"] == produto_id


# CADASTRAR PRODUTO (com token de admin)

def test_cadastrar_produto_com_token(token_admin):
    payload = {
        "nome": f"Produto {uuid.uuid4()}",
        "preco": 150,
        "descricao": "Produto criado em teste automatizado",
        "quantidade": 5
    }
    headers = {"Authorization": token_admin}
    response = requests.post(f"{ENDPOINT}/produtos", json=payload, headers=headers)

    assert response.status_code == 201
    assert response.json()["message"] == "Cadastro realizado com sucesso"


# CADASTRAR PRODUTO SEM TOKEN

def test_cadastrar_produto_sem_token():
    payload = {
        "nome": f"Produto {uuid.uuid4()}",
        "preco": 150,
        "descricao": "Produto sem auth",
        "quantidade": 5
    }
    response = requests.post(f"{ENDPOINT}/produtos", json=payload)

    assert response.status_code == 401


# EDITAR PRODUTO (com token de admin)

def test_editar_produto_com_token(token_admin):
    produto_id = criar_produto(token_admin)
    payload = {
        "nome": f"Produto Atualizado {uuid.uuid4()}",
        "preco": 200,
        "descricao": "Produto atualizado em teste",
        "quantidade": 20
    }
    headers = {"Authorization": token_admin}
    response = requests.put(f"{ENDPOINT}/produtos/{produto_id}", json=payload, headers=headers)

    assert response.status_code == 200


# EXCLUIR PRODUTO (com token de admin)

def test_excluir_produto_com_token(token_admin):
    produto_id = criar_produto(token_admin)
    headers = {"Authorization": token_admin}
    response = requests.delete(f"{ENDPOINT}/produtos/{produto_id}", headers=headers)

    assert response.status_code == 200


# BUSCAR PRODUTO INEXISTENTE

def test_buscar_produto_inexistente():
    response = requests.get(f"{ENDPOINT}/produtos/000000000000000000000000")

    assert response.status_code == 400
