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

def criar_carrinho_helper():
    """
    Cria um usuário, faz login, cria um produto e abre um carrinho.
    Retorna o _id do carrinho criado.
    """
    # 1. Cria usuário admin e obtém token
    email = gerar_email()
    password = "teste123"
    requests.post(f"{ENDPOINT}/usuarios", json={
        "nome": "Usuario Carrinho Teste",
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


# ==========================================
#  LOGIN
# ==========================================

def criar_usuario_retorna_credenciais():
    """Cria um usuário e retorna email e senha para uso nos testes de login."""
    email = gerar_email()
    password = "teste123"
    requests.post(f"{ENDPOINT}/usuarios", json={
        "nome": "Usuario Login Teste",
        "email": email,
        "password": password,
        "administrador": "true"
    })
    return email, password


#  LOGIN COM CREDENCIAIS CORRETAS

def test_login_credenciais_corretas():
    email, password = criar_usuario_retorna_credenciais()
    response = requests.post(
        f"{ENDPOINT}/login",
        json={"email": email, "password": password}
    )
    assert response.status_code == 200
    assert "authorization" in response.json()
    assert response.json()["message"] == "Login realizado com sucesso"


#  LOGIN COM SENHA ERRADA

def test_login_senha_errada():
    email, _ = criar_usuario_retorna_credenciais()
    response = requests.post(
        f"{ENDPOINT}/login",
        json={"email": email, "password": "senhaerrada"}
    )
    assert response.status_code == 401


#  LOGIN COM EMAIL INEXISTENTE

def test_login_email_inexistente():
    response = requests.post(
        f"{ENDPOINT}/login",
        json={"email": f"naoexiste_{uuid.uuid4().hex[:8]}@email.com", "password": "123456"}
    )
    assert response.status_code == 401


#  LOGIN SEM CAMPO EMAIL

def test_login_sem_email():
    response = requests.post(
        f"{ENDPOINT}/login",
        json={"password": "123456"}
    )
    assert response.status_code == 400


#  LOGIN SEM CAMPO SENHA

def test_login_sem_senha():
    response = requests.post(
        f"{ENDPOINT}/login",
        json={"email": gerar_email()}
    )
    assert response.status_code == 400


#  LOGIN COM CAMPOS VAZIOS

def test_login_campos_vazios():
    response = requests.post(
        f"{ENDPOINT}/login",
        json={"email": "", "password": ""}
    )
    assert response.status_code == 400


# ==========================================
#  PRODUTOS (com autenticação)
# ==========================================

def obter_token():
    """Cria um usuário admin, faz login e retorna o Bearer token."""
    email = gerar_email()
    password = "teste123"
    requests.post(f"{ENDPOINT}/usuarios", json={
        "nome": "Admin Produto Teste",
        "email": email,
        "password": password,
        "administrador": "true"
    })
    response = requests.post(
        f"{ENDPOINT}/login",
        json={"email": email, "password": password}
    )
    return response.json()["authorization"]


def criar_produto_helper(token):
    """Cria um produto e retorna seu _id."""
    payload = {
        "nome": f"Produto {uuid.uuid4().hex[:8]}",
        "preco": 100,
        "descricao": "Produto de teste",
        "quantidade": 10
    }
    response = requests.post(
        f"{ENDPOINT}/produtos",
        json=payload,
        headers={"Authorization": token}
    )
    return response.json()["_id"]


#  CADASTRAR PRODUTO COM TOKEN

def test_cadastrar_produto_com_token():
    token = obter_token()
    payload = {
        "nome": f"Produto {uuid.uuid4().hex[:8]}",
        "preco": 150,
        "descricao": "Produto criado com autenticação",
        "quantidade": 5
    }
    response = requests.post(
        f"{ENDPOINT}/produtos",
        json=payload,
        headers={"Authorization": token}
    )
    assert response.status_code == 201
    assert response.json()["message"] == "Cadastro realizado com sucesso"


#  CADASTRAR PRODUTO SEM TOKEN

def test_cadastrar_produto_sem_token():
    payload = {
        "nome": f"Produto {uuid.uuid4().hex[:8]}",
        "preco": 150,
        "descricao": "Produto sem autenticação",
        "quantidade": 5
    }
    response = requests.post(
        f"{ENDPOINT}/produtos",
        json=payload
    )
    assert response.status_code == 401


#  EDITAR PRODUTO COM TOKEN

def test_editar_produto_com_token():
    token = obter_token()
    produto_id = criar_produto_helper(token)
    payload = {
        "nome": f"Produto Atualizado {uuid.uuid4().hex[:8]}",
        "preco": 200,
        "descricao": "Produto atualizado",
        "quantidade": 20
    }
    response = requests.put(
        f"{ENDPOINT}/produtos/{produto_id}",
        json=payload,
        headers={"Authorization": token}
    )
    assert response.status_code == 200


#  EXCLUIR PRODUTO COM TOKEN

def test_excluir_produto_com_token():
    token = obter_token()
    produto_id = criar_produto_helper(token)
    response = requests.delete(
        f"{ENDPOINT}/produtos/{produto_id}",
        headers={"Authorization": token}
    )
    assert response.status_code == 200


#  BUSCAR PRODUTO INEXISTENTE

def test_buscar_produto_inexistente():
    response = requests.get(
        f"{ENDPOINT}/produtos/000000000000000000000000"
    )
    assert response.status_code == 400
