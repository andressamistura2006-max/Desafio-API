import time
import requests

from helpers.config import ENDPOINT
from helpers.usuarios import gerar_email

# Senha padrão usada em todos os usuários criados nos testes
SENHA_PADRAO = "teste123"

# Retry para lidar com latência de propagação da API remota
_MAX_RETRIES = 5
_RETRY_DELAY = 3  # segundos entre tentativas


def fazer_login(email: str, password: str) -> requests.Response:
    """Faz login e retorna o objeto Response completo."""
    return requests.post(f"{ENDPOINT}/login", json={"email": email, "password": password})


def obter_token_admin() -> str:
    """
    Cria um usuário administrador, faz login e retorna o Bearer token.
    Usa retry com delay para lidar com latência de propagação da API.
    Executada uma única vez por sessão via fixture do conftest.
    """
    email = gerar_email()
    body = {}

    # Cria o usuário admin
    requests.post(f"{ENDPOINT}/usuarios", json={
        "nome": "Admin Token Teste",
        "email": email,
        "password": SENHA_PADRAO,
        "administrador": "true"
    })

    # Tenta fazer login com retry para lidar com latência da API
    for tentativa in range(1, _MAX_RETRIES + 1):
        time.sleep(_RETRY_DELAY)
        response = fazer_login(email, SENHA_PADRAO)
        body = response.json()

        if "authorization" in body:
            return body["authorization"]

    raise RuntimeError(
        f"Não foi possível obter token após {_MAX_RETRIES} tentativas. "
        f"Última resposta: {body}"
    )
