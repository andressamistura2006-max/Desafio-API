import pytest

from helpers.auth import obter_token_admin


@pytest.fixture(scope="session")
def token_admin():
    """
    Fixture de sessão: cria um usuário admin, faz login e retorna o token.
    Executada uma única vez por sessão de testes, compartilhada entre todos
    os testes que a declararem como parâmetro.
    """
    return obter_token_admin()
