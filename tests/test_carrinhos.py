import requests
import uuid

from helpers.config import ENDPOINT


# LISTAR CARRINHOS

def test_listar_carrinhos():
    response = requests.get(f"{ENDPOINT}/carrinhos")

    assert response.status_code == 200
    assert "carrinhos" in response.json()


# BUSCAR CARRINHO POR ID

def criar_carrinho_helper():
    """
    Cria um usuário, faz login, cria um produto e abre um carrinho.
    Retorna o _id do carrinho criado.
    """
    from helpers.usuarios import gerar_email

    email = gerar_email()
    password = "teste123"

    # 1. Cria usuário admin e obtém token
    requests.post(f"{ENDPOINT}/usuarios", json={
        "nome": "Andressa Carrinho",
        "email": email,
        "password": password,
        "administrador": "true"
    })
    login = requests.post(f"{ENDPOINT}/login", json={"email": email, "password": password})
    token = login.json()["authorization"]

    # 2. Cria um produto com o token
    produto = requests.post(f"{ENDPOINT}/produtos", json={
        "nome": f"Produto Carrinho {uuid.uuid4().hex[:8]}",
        "preco": 50,
        "descricao": "Produto para teste de carrinho",
        "quantidade": 10
    }, headers={"Authorization": token})
    produto_id = produto.json()["_id"]

    # 3. Cria o carrinho com o produto
    carrinho = requests.post(f"{ENDPOINT}/carrinhos", json={
        "produtos": [{"idProduto": produto_id, "quantidade": 1}]
    }, headers={"Authorization": token})

    return carrinho.json()["_id"]


def test_buscar_carrinho_por_id():
    carrinho_id = criar_carrinho_helper()
    busca = requests.get(f"{ENDPOINT}/carrinhos/{carrinho_id}")

    assert busca.status_code == 200
    assert busca.json()["_id"] == carrinho_id
