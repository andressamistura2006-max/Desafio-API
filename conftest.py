import pytest
import requests

from helpers.auth import obter_token_admin, SENHA_PADRAO
from helpers.config import ENDPOINT
from helpers.usuarios import gerar_email
from helpers.produtos import criar_produto


@pytest.fixture(scope="session")
def token_admin():
    """
    Cria um usuário admin, faz login e retorna o Bearer token.
    Executada uma única vez por sessão — compartilhada por todos
    os testes que precisam de autenticação.
    """
    return obter_token_admin()


@pytest.fixture(scope="session")
def usuario_login():
    """
    Cria um usuário uma única vez para os testes de login.
    Retorna (email, password) para reutilização em múltiplos testes.
    """
    email = gerar_email()
    password = SENHA_PADRAO
    requests.post(f"{ENDPOINT}/usuarios", json={
        "nome": "Andressa Login",
        "email": email,
        "password": password,
        "administrador": "true"
    })
    return email, password


@pytest.fixture(scope="session")
def produto_admin(token_admin):
    """
    Cria um produto uma única vez por sessão para testes que
    precisam de um produto existente (editar, excluir, carrinho).
    """
    return criar_produto(token_admin)
