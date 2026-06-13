import requests

from helpers.config import ENDPOINT
from helpers.usuarios import gerar_email
from helpers.auth import SENHA_PADRAO


# LOGIN COM CREDENCIAIS CORRETAS
# Reutiliza o usuário criado pela fixture — sem criar novo usuário aqui

def test_login_credenciais_corretas(usuario_login):
    email, password = usuario_login
    response = requests.post(f"{ENDPOINT}/login", json={"email": email, "password": password})

    assert response.status_code == 200
    assert "authorization" in response.json()
    assert response.json()["message"] == "Login realizado com sucesso"


# LOGIN COM SENHA ERRADA

def test_login_senha_errada(usuario_login):
    email, _ = usuario_login
    response = requests.post(f"{ENDPOINT}/login", json={"email": email, "password": "senhaerrada"})

    assert response.status_code == 401


# LOGIN COM EMAIL INEXISTENTE

def test_login_email_inexistente():
    response = requests.post(
        f"{ENDPOINT}/login",
        json={"email": f"naoexiste_{gerar_email()}", "password": SENHA_PADRAO}
    )

    assert response.status_code == 401


# LOGIN SEM EMAIL

def test_login_sem_email():
    response = requests.post(
        f"{ENDPOINT}/login",
        json={"password": SENHA_PADRAO}
    )

    assert response.status_code == 400


# LOGIN SEM SENHA

def test_login_sem_senha():
    response = requests.post(
        f"{ENDPOINT}/login",
        json={"email": gerar_email()}
    )

    assert response.status_code == 400


# LOGIN COM CAMPOS VAZIOS

def test_login_campos_vazios():
    response = requests.post(
        f"{ENDPOINT}/login",
        json={"email": "", "password": ""}
    )

    assert response.status_code == 400
