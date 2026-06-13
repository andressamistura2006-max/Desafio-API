import requests
import uuid

from helpers.config import ENDPOINT
from helpers.usuarios import gerar_email


# ==========================================
#  HELPER
# ==========================================

def criar_setup_carrinho():
    """
    Cria um usuário admin, faz login, cria um produto e retorna
    o token e o id do produto para uso nos testes de carrinho.
    """
    email = gerar_email()
    password = "teste123"

    requests.post(f"{ENDPOINT}/usuarios", json={
        "nome": "Andressa Carrinho",
        "email": email,
        "password": password,
        "administrador": "true"
    })
    login = requests.post(f"{ENDPOINT}/login", json={"email": email, "password": password})
    token = login.json()["authorization"]

    produto = requests.post(f"{ENDPOINT}/produtos", json={
        "nome": f"Produto Carrinho {uuid.uuid4().hex[:8]}",
        "preco": 50,
        "descricao": "Produto para teste de carrinho",
        "quantidade": 10
    }, headers={"Authorization": token})
    produto_id = produto.json()["_id"]

    return token, produto_id


# ==========================================
#  LISTAR CARRINHOS
# ==========================================

def test_listar_carrinhos():
    response = requests.get(f"{ENDPOINT}/carrinhos")

    assert response.status_code == 200
    assert "carrinhos" in response.json()


# ==========================================
#  BUSCAR CARRINHO POR ID
# ==========================================

def test_buscar_carrinho_por_id():
    token, produto_id = criar_setup_carrinho()

    carrinho = requests.post(f"{ENDPOINT}/carrinhos", json={
        "produtos": [{"idProduto": produto_id, "quantidade": 1}]
    }, headers={"Authorization": token})
    carrinho_id = carrinho.json()["_id"]

    busca = requests.get(f"{ENDPOINT}/carrinhos/{carrinho_id}")

    assert busca.status_code == 200
    assert busca.json()["_id"] == carrinho_id


# ==========================================
#  CRIAR CARRINHO
# ==========================================

def test_criar_carrinho():
    token, produto_id = criar_setup_carrinho()

    response = requests.post(f"{ENDPOINT}/carrinhos", json={
        "produtos": [{"idProduto": produto_id, "quantidade": 2}]
    }, headers={"Authorization": token})

    assert response.status_code == 201
    assert response.json()["message"] == "Cadastro realizado com sucesso"


def test_criar_carrinho_sem_token():
    response = requests.post(f"{ENDPOINT}/carrinhos", json={
        "produtos": [{"idProduto": "qualquerid", "quantidade": 1}]
    })

    assert response.status_code == 401


def test_criar_dois_carrinhos_mesmo_usuario():
    token, produto_id = criar_setup_carrinho()

    requests.post(f"{ENDPOINT}/carrinhos", json={
        "produtos": [{"idProduto": produto_id, "quantidade": 1}]
    }, headers={"Authorization": token})

    response = requests.post(f"{ENDPOINT}/carrinhos", json={
        "produtos": [{"idProduto": produto_id, "quantidade": 1}]
    }, headers={"Authorization": token})

    assert response.status_code == 400
    assert response.json()["message"] == "Não é permitido ter mais de 1 carrinho"


# ==========================================
#  CONCLUIR COMPRA
# ==========================================

def test_concluir_compra():
    token, produto_id = criar_setup_carrinho()

    requests.post(f"{ENDPOINT}/carrinhos", json={
        "produtos": [{"idProduto": produto_id, "quantidade": 1}]
    }, headers={"Authorization": token})

    response = requests.delete(
        f"{ENDPOINT}/carrinhos/concluir-compra",
        headers={"Authorization": token}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Registro excluído com sucesso"


# ==========================================
#  CANCELAR COMPRA
# ==========================================

def test_cancelar_compra():
    token, produto_id = criar_setup_carrinho()

    requests.post(f"{ENDPOINT}/carrinhos", json={
        "produtos": [{"idProduto": produto_id, "quantidade": 1}]
    }, headers={"Authorization": token})

    response = requests.delete(
        f"{ENDPOINT}/carrinhos/cancelar-compra",
        headers={"Authorization": token}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Registro excluído com sucesso. Estoque dos produtos reabastecido"
