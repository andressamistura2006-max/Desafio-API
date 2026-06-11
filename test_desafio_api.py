import requests
import uuid

ENDPOINT = "https://compassuol.serverest.dev"


def gerar_email():
    return f"teste_{uuid.uuid4()}@email.com"

def criar_usuario():
    payload = {
        "nome": "Usuario Teste",
        "email": gerar_email(),
        "password": "123456",
        "administrador": "true"
    }
    response = requests.post(
        f"{ENDPOINT}/usuarios",
        json=payload
    )
    return response.json()["_id"]

#   CRIAR USUÁRIO

def test_cadastrar_usuario():
    payload = {
        "nome": "Andressa",
        "email": gerar_email(),
        "password": "123456",
        "administrador": "true"
    }
    response = requests.post(
        f"{ENDPOINT}/usuarios",
        json=payload
    )
    assert response.status_code == 201
    assert response.json()["message"] == "Cadastro realizado com sucesso"


#  LISTAR USUÁRIO POR ID

def test_buscar_usuario_por_id():
    user_id = criar_usuario()
    response = requests.get(
        f"{ENDPOINT}/usuarios/{user_id}"
    )
    assert response.status_code == 200
    assert response.json()["_id"] == user_id


#  EXCLUIR USUÁRIO

def test_excluir_usuario():
    user_id = criar_usuario()

    response = requests.delete(
        f"{ENDPOINT}/usuarios/{user_id}"
    )
    assert response.status_code == 200

#  EDITAR USUÁRIO

def test_editar_usuario():
    user_id = criar_usuario()
    payload = {
        "nome": "Usuario Atualizado",
        "email": gerar_email(),
        "password": "123456",
        "administrador": "true"
    }
    response = requests.put(
        f"{ENDPOINT}/usuarios/{user_id}",
        json=payload
    )
    assert response.status_code == 200


#  LISTAR PRODUTOS

def test_listar_produtos():
    response = requests.get(
        f"{ENDPOINT}/produtos"
    )
    assert response.status_code == 200
    assert "produtos" in response.json()

# BUSCAR PRODUTO POR ID

def test_buscar_produto_por_id():
    response = requests.get(
        f"{ENDPOINT}/produtos"
    )
    produto_id = response.json()["produtos"][0]["_id"]
    busca = requests.get(
        f"{ENDPOINT}/produtos/{produto_id}"
    )
    assert busca.status_code == 200
    assert busca.json()["_id"] == produto_id

#  LISTAR CARRINHO

def test_listar_carrinhos():
    response = requests.get(
        f"{ENDPOINT}/carrinhos"
    )
    assert response.status_code == 200
    assert "carrinhos" in response.json()

#  LISTAR CARRINHO POR ID

def test_buscar_carrinho_por_id():
    response = requests.get(
        f"{ENDPOINT}/carrinhos"
    )
    carrinho_id = response.json()["carrinhos"][0]["_id"]
    busca = requests.get(
        f"{ENDPOINT}/carrinhos/{carrinho_id}"
    )
    assert busca.status_code == 200
    assert busca.json()["_id"] == carrinho_id

#  EMAIL DUPLICADO

def test_cadastrar_usuario_email_duplicado():
    email = gerar_email()
    payload = {
        "nome": "Usuario Teste",
        "email": email,
        "password": "123456",
        "administrador": "true"
    }
    requests.post(
        f"{ENDPOINT}/usuarios",
        json=payload
    )
    response = requests.post(
        f"{ENDPOINT}/usuarios",
        json=payload
    )
    assert response.status_code == 400
    assert response.json()["message"] == "Este email já está sendo usado"

#  CADASTRO SEM EMAIL

def test_cadastrar_usuario_sem_email():
    payload = {
        "nome": "Usuario Teste",
        "password": "123456",
        "administrador": "true"
    }
    response = requests.post(
        f"{ENDPOINT}/usuarios",
        json=payload
    )
    print(response.status_code)
    print(response.json())
    assert response.status_code == 400

#  BUSCAR USUÁRIO INEXISTENTE

def test_buscar_usuario_inexistente():
    response = requests.get(
        f"{ENDPOINT}/usuarios/000000000000000000000000"
    )
    body = response.json()
    assert response.status_code == 400
    assert body is not None