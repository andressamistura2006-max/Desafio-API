import requests
import uuid

from helpers.config import ENDPOINT
from helpers.usuarios import gerar_email


# ==========================================
#  HELPER
# ==========================================

def criar_produto_para_carrinho(token: str) -> str:
    """Cria um produto e retorna seu _id. Reutiliza token já obtido."""
    produto = requests.post(f"{ENDPOINT}/produtos", json={
        "nome": f"Produto Carrinho {uuid.uuid4().hex[:8]}",
        "preco": 50,
        "descricao": "Produto para teste de carrinho",
        "quantidade": 10
    }, headers={"Authorization": token})
    return produto.json()["_id"]


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

def test_buscar_carrinho_por_id(token_admin):
    produto_id = criar_produto_para_carrinho(token_admin)

    carrinho = requests.post(f"{ENDPOINT}/carrinhos", json={
        "produtos": [{"idProduto": produto_id, "quantidade": 1}]
    }, headers={"Authorization": token_admin})
    carrinho_id = carrinho.json()["_id"]

    busca = requests.get(f"{ENDPOINT}/carrinhos/{carrinho_id}")

    # Limpa o carrinho após a busca
    requests.delete(f"{ENDPOINT}/carrinhos/cancelar-compra", headers={"Authorization": token_admin})

    assert busca.status_code == 200
    assert busca.json()["_id"] == carrinho_id


# ==========================================
#  CRIAR CARRINHO
# ==========================================

def test_criar_carrinho(token_admin):
    produto_id = criar_produto_para_carrinho(token_admin)

    response = requests.post(f"{ENDPOINT}/carrinhos", json={
        "produtos": [{"idProduto": produto_id, "quantidade": 2}]
    }, headers={"Authorization": token_admin})

    # Limpa após o teste
    requests.delete(f"{ENDPOINT}/carrinhos/cancelar-compra", headers={"Authorization": token_admin})

    assert response.status_code == 201
    assert response.json()["message"] == "Cadastro realizado com sucesso"


def test_criar_carrinho_sem_token():
    response = requests.post(f"{ENDPOINT}/carrinhos", json={
        "produtos": [{"idProduto": "qualquerid", "quantidade": 1}]
    })

    assert response.status_code == 401


def test_criar_dois_carrinhos_mesmo_usuario(token_admin):
    produto_id = criar_produto_para_carrinho(token_admin)

    # Cria o primeiro carrinho
    requests.post(f"{ENDPOINT}/carrinhos", json={
        "produtos": [{"idProduto": produto_id, "quantidade": 1}]
    }, headers={"Authorization": token_admin})

    # Tenta criar um segundo — deve retornar 400
    response = requests.post(f"{ENDPOINT}/carrinhos", json={
        "produtos": [{"idProduto": produto_id, "quantidade": 1}]
    }, headers={"Authorization": token_admin})

    # Limpa após o teste
    requests.delete(f"{ENDPOINT}/carrinhos/cancelar-compra", headers={"Authorization": token_admin})

    assert response.status_code == 400
    assert response.json()["message"] == "Não é permitido ter mais de 1 carrinho"


# ==========================================
#  CONCLUIR COMPRA
# ==========================================

def test_concluir_compra(token_admin):
    produto_id = criar_produto_para_carrinho(token_admin)

    requests.post(f"{ENDPOINT}/carrinhos", json={
        "produtos": [{"idProduto": produto_id, "quantidade": 1}]
    }, headers={"Authorization": token_admin})

    response = requests.delete(
        f"{ENDPOINT}/carrinhos/concluir-compra",
        headers={"Authorization": token_admin}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Registro excluído com sucesso"


# ==========================================
#  CANCELAR COMPRA
# ==========================================

def test_cancelar_compra(token_admin):
    produto_id = criar_produto_para_carrinho(token_admin)

    requests.post(f"{ENDPOINT}/carrinhos", json={
        "produtos": [{"idProduto": produto_id, "quantidade": 1}]
    }, headers={"Authorization": token_admin})

    response = requests.delete(
        f"{ENDPOINT}/carrinhos/cancelar-compra",
        headers={"Authorization": token_admin}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Registro excluído com sucesso. Estoque dos produtos reabastecido"
