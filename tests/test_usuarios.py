import requests

from helpers.config import ENDPOINT
from helpers.usuarios import gerar_email, criar_usuario


# CRIAR USUÁRIO

def test_cadastrar_usuario():
    payload = {
        "nome": "Andressa",
        "email": gerar_email(),
        "password": "123456",
        "administrador": "true"
    }
    response = requests.post(f"{ENDPOINT}/usuarios", json=payload)

    assert response.status_code == 201
    assert response.json()["message"] == "Cadastro realizado com sucesso"


# LISTAR USUÁRIO POR ID

def test_buscar_usuario_por_id():
    user_id = criar_usuario()
    response = requests.get(f"{ENDPOINT}/usuarios/{user_id}")

    assert response.status_code == 200
    assert response.json()["_id"] == user_id


# EXCLUIR USUÁRIO

def test_excluir_usuario():
    user_id = criar_usuario()
    response = requests.delete(f"{ENDPOINT}/usuarios/{user_id}")

    assert response.status_code == 200


# EDITAR USUÁRIO

def test_editar_usuario():
    user_id = criar_usuario()
    payload = {
        "nome": "Usuario Atualizado",
        "email": gerar_email(),
        "password": "123456",
        "administrador": "true"
    }
    response = requests.put(f"{ENDPOINT}/usuarios/{user_id}", json=payload)

    # A API retorna 200 ao atualizar um usuário existente
    assert response.status_code == 200
    assert response.json()["message"] == "Registro alterado com sucesso"


# EMAIL DUPLICADO

def test_cadastrar_usuario_email_duplicado():
    email = gerar_email()
    payload = {
        "nome": "Usuario Teste",
        "email": email,
        "password": "123456",
        "administrador": "true"
    }
    requests.post(f"{ENDPOINT}/usuarios", json=payload)
    response = requests.post(f"{ENDPOINT}/usuarios", json=payload)

    assert response.status_code == 400
    assert response.json()["message"] == "Este email já está sendo usado"


# CADASTRO SEM EMAIL

def test_cadastrar_usuario_sem_email():
    payload = {
        "nome": "Usuario Teste",
        "password": "123456",
        "administrador": "true"
    }
    response = requests.post(f"{ENDPOINT}/usuarios", json=payload)

    assert response.status_code == 400


# BUSCAR USUÁRIO INEXISTENTE

def test_buscar_usuario_inexistente():
    response = requests.get(f"{ENDPOINT}/usuarios/000000000000000000000000")

    assert response.status_code == 400
    assert response.json() is not None
