import requests

from helpers.config import ENDPOINT


# LISTAR CARRINHOS

def test_listar_carrinhos():
    response = requests.get(f"{ENDPOINT}/carrinhos")

    assert response.status_code == 200
    assert "carrinhos" in response.json()


# BUSCAR CARRINHO POR ID

def test_buscar_carrinho_por_id():
    response = requests.get(f"{ENDPOINT}/carrinhos")
    carrinhos = response.json()["carrinhos"]

    if not carrinhos:
        import pytest
        pytest.skip("Nenhum carrinho disponível na API para buscar por ID")

    carrinho_id = carrinhos[0]["_id"]
    busca = requests.get(f"{ENDPOINT}/carrinhos/{carrinho_id}")

    assert busca.status_code == 200
    assert busca.json()["_id"] == carrinho_id
