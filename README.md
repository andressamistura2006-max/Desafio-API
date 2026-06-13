# Desafio API - Testes Automatizados (ServeRest)

![Testes](https://github.com/andressamistura2006-max/Desafio-API/actions/workflows/tests.yml/badge.svg)

Suite de testes automatizados de API REST usando Python, Pytest e Requests, com base na API publica ServeRest. A suite cobre fluxos de autenticacao, usuarios, produtos e carrinhos, com cenarios positivos e negativos.

---

## API utilizada

`https://compassuol.serverest.dev`

---

## Tecnologias utilizadas

- Python 3.10+
- Pytest
- Requests
- UUID
- Jsonschema
- GitHub Actions

---

## Instalacao

```bash
git clone https://github.com/andressamistura2006-max/Desafio-API.git
cd Desafio-API
pip install -r requirements.txt
```

---

## Execucao dos testes

```bash
# Todos os testes oficiais
pytest

# Com saida detalhada
pytest -v

# Com logs/prints
pytest -v -s

# Um modulo especifico
pytest tests/test_login.py -v
```

O arquivo `test_desafio_api.py` foi mantido como legado da primeira versao da suite. A coleta padrao do Pytest esta configurada em `pytest.ini` para executar apenas os testes dentro de `tests/`.

---

## Estrutura do projeto

```text
Desafio-API/
|-- .github/workflows/
|   `-- tests.yml             # pipeline de CI
|-- helpers/
|   |-- config.py             # URL base da API
|   |-- auth.py               # login, token de admin e senha padrao
|   |-- usuarios.py           # gerar_email(), criar_usuario()
|   `-- produtos.py           # criar_produto(token)
|-- tests/
|   |-- test_usuarios.py      # CRUD de usuarios + cenarios negativos
|   |-- test_login.py         # cenarios de autenticacao
|   |-- test_produtos.py      # produtos com e sem token
|   |-- test_carrinhos.py     # carrinhos — criar, buscar, concluir, cancelar
|   `-- test_schemas.py       # validacao de contrato JSON Schema
|-- conftest.py               # fixture token_admin
|-- pytest.ini                # coleta oficial apenas em tests/
|-- PLANO-DE-TESTES.md        # planejamento da suite
|-- test_desafio_api.py       # arquivo legado
`-- requirements.txt
```

---

## Cobertura de testes

### Metodo utilizado

A cobertura foi calculada com base em cenarios por endpoint: para cada operacao da API, foram mapeados cenarios de sucesso, validacao, autorizacao e recurso inexistente.

### Mapeamento de cobertura

| Endpoint | Operacao | Cenarios mapeados | Cenarios cobertos | Cobertura |
|---|---|---:|---:|---:|
| `POST /usuarios` | Criar usuario | 3 | 3 | 100% |
| `GET /usuarios/{id}` | Buscar por ID | 2 | 2 | 100% |
| `PUT /usuarios/{id}` | Atualizar usuario | 1 | 1 | 100% |
| `DELETE /usuarios/{id}` | Excluir usuario | 1 | 1 | 100% |
| `POST /login` | Autenticar | 6 | 6 | 100% |
| `GET /produtos` | Listar produtos | 1 | 1 | 100% |
| `GET /produtos/{id}` | Buscar por ID | 2 | 2 | 100% |
| `POST /produtos` | Criar produto | 2 | 2 | 100% |
| `PUT /produtos/{id}` | Atualizar produto | 1 | 1 | 100% |
| `DELETE /produtos/{id}` | Excluir produto | 1 | 1 | 100% |
| `GET /carrinhos` | Listar carrinhos | 1 | 1 | 100% |
| `GET /carrinhos/{id}` | Buscar por ID | 1 | 1 | 100% |
| `POST /carrinhos` | Criar carrinho | 2 | 2 | 100% |
| `DELETE /carrinhos/concluir-compra` | Concluir compra | 1 | 1 | 100% |
| `DELETE /carrinhos/cancelar-compra` | Cancelar compra | 1 | 1 | 100% |

**Total: 26 cenarios cobertos de 26 mapeados**

### Cobertura total

> 26 / 26 cenarios mapeados = **100%**

### O que ficou fora e por que

Todos os cenarios mapeados foram cobertos nesta versao da suite.

---

## Cenarios testados

### Usuarios (7 testes)

- Cadastro com sucesso
- Busca por ID existente
- Atualizacao de dados
- Exclusao
- Email duplicado (400)
- Campo email ausente (400)
- ID inexistente (400)

### Login (6 testes)

- Credenciais corretas (200 + token)
- Senha errada (401)
- Email inexistente (401)
- Sem campo email (400)
- Sem campo senha (400)
- Campos vazios (400)

### Produtos (7 testes)

- Listagem
- Busca por ID
- Cadastro com token de admin (201)
- Cadastro sem token (401)
- Atualizacao com token
- Exclusao com token
- ID inexistente (400)

### Carrinhos (6 testes)

- Listagem
- Busca por ID
- Criar carrinho com token (201)
- Criar carrinho sem token (401)
- Tentar criar dois carrinhos para o mesmo usuário (400)
- Concluir compra
- Cancelar compra

### Contrato / JSON Schema (3 testes)

- Estrutura da resposta de `POST /usuarios` — valida campos `message` e `_id` com tipos corretos
- Estrutura da resposta de `POST /login` — valida campos `message` e `authorization`
- Estrutura da resposta de `GET /produtos` — valida o array `produtos` e os campos de cada item

---

## Bugs observados na API

Durante a analise da API, foram observados comportamentos que podem ser considerados inconsistentes em relacao a convencoes REST.

### Bug 1 - PUT /usuarios/{id} cria usuario quando o ID nao existe

**Endpoint:** `PUT /usuarios/000000000000000000000000`

**Resultado esperado:** `404 Not Found`, pois o recurso nao existe.

**Resultado obtido:** `201 Created`, criando um novo usuario.

**Severidade:** Alta. Uma operacao de atualizacao passa a se comportar como criacao.

### Bug 2 - DELETE /usuarios/{id} retorna 200 para ID inexistente

**Endpoint:** `DELETE /usuarios/000000000000000000000000`

**Resultado esperado:** `404 Not Found`, pois o recurso nao existe.

**Resultado obtido:** `200 OK` com a mensagem `"Nenhum registro excluido"`.

**Severidade:** Media. Nao causa perda de dados, mas pode induzir falsa percepcao de sucesso.

---

## CI/CD

A suite e executada automaticamente via GitHub Actions a cada push ou pull request.

Consulte `.github/workflows/tests.yml` para ver a configuracao do pipeline.

---

## Autor

Andressa Mistura
