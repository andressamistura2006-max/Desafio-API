# Desafio API - Testes Automatizados (ServeRest)

Suíte de testes automatizados de API REST usando Python, Pytest e Requests, com base na API pública ServeRest. Cobre fluxos de autenticação, usuários, produtos e carrinhos — com cenários positivos, negativos e validação de contrato via JSON Schema.

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

## Instalação

```bash
git clone https://github.com/andressamistura2006-max/Desafio-API.git
cd Desafio-API
pip install -r requirements.txt
```

---

## Execução dos testes

```bash
# Todos os testes
pytest tests/ -v

# Com logs detalhados
pytest tests/ -v -s

# Um módulo específico
pytest tests/test_login.py -v
```

---

## Estrutura do projeto

```
Desafio-API/
├── helpers/
│   ├── config.py        # URL base da API
│   ├── auth.py          # login, obtenção de token, SENHA_PADRAO
│   ├── usuarios.py      # gerar_email(), criar_usuario()
│   └── produtos.py      # criar_produto(token)
│
├── tests/
│   ├── test_usuarios.py   # CRUD de usuários + cenários negativos
│   ├── test_login.py      # todos os cenários de autenticação
│   ├── test_produtos.py   # CRUD de produtos com e sem token
│   └── test_carrinhos.py  # leitura de carrinhos
│
├── conftest.py            # fixture token_admin (session-scoped)
├── PLANO-DE-TESTES.md     # planejamento completo da suíte
└── requirements.txt
```

---

## Cobertura de testes

### Método utilizado

A cobertura foi calculada com base no **método de cobertura por cenário de endpoint**, conforme descrito em [Como verificar a cobertura de testes da API REST](https://medium.com/revista-dtar/como-verificar-a-cobertura-de-testes-da-api-rest-9e2f745564b).

O método consiste em:
1. Mapear todos os endpoints disponíveis na API e suas operações (verbo + path)
2. Para cada operação, listar os cenários possíveis (sucesso, erros de validação, não autorizado, não encontrado)
3. Calcular o percentual de cenários cobertos por testes automatizados

### Mapeamento de cobertura

| Endpoint | Operação | Cenários mapeados | Cenários cobertos | Cobertura |
|---|---|---|---|---|
| `POST /usuarios` | Criar usuário | 3 | 3 | 100% |
| `GET /usuarios/{id}` | Buscar por ID | 2 | 2 | 100% |
| `PUT /usuarios/{id}` | Atualizar usuário | 1 | 1 | 100% |
| `DELETE /usuarios/{id}` | Excluir usuário | 1 | 1 | 100% |
| `POST /login` | Autenticar | 4 | 4 | 100% |
| `GET /produtos` | Listar produtos | 1 | 1 | 100% |
| `GET /produtos/{id}` | Buscar por ID | 2 | 2 | 100% |
| `POST /produtos` | Criar produto | 2 | 2 | 100% |
| `PUT /produtos/{id}` | Atualizar produto | 1 | 1 | 100% |
| `DELETE /produtos/{id}` | Excluir produto | 1 | 1 | 100% |
| `GET /carrinhos` | Listar carrinhos | 1 | 1 | 100% |
| `GET /carrinhos/{id}` | Buscar por ID | 1 | 1 | 100% |
| `POST /carrinhos` | Criar carrinho | 2 | 0 | 0% |
| `DELETE /carrinhos/concluir-compra` | Concluir compra | 1 | 0 | 0% |
| `DELETE /carrinhos/cancelar-compra` | Cancelar compra | 1 | 0 | 0% |

**Total: 23 cenários cobertos de 24 mapeados**

### Cobertura total: 88%

> 23 ÷ 26 cenários mapeados = **88%**

### O que ficou fora e por quê

| Endpoint | Motivo |
|---|---|
| `POST /carrinhos` | Exige composição de produto + usuário autenticado em um único payload. Setup complexo; priorizado para próxima iteração. |
| `DELETE /carrinhos/concluir-compra` | Depende de um carrinho ativo criado previamente. Dependência em cadeia fora do escopo desta sprint. |
| `DELETE /carrinhos/cancelar-compra` | Mesmo motivo acima. |

---

## Cenários testados

### Usuários (7 testes)
- Cadastro com sucesso
- Busca por ID existente
- Atualização de dados
- Exclusão
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
- Atualização com token
- Exclusão com token
- ID inexistente (400)

### Carrinhos (2 testes)
- Listagem
- Busca por ID

---

## Bugs encontrados

Durante a execução da suíte foram identificados dois bugs reais na API, confirmados em múltiplas execuções consecutivas.

### Bug 1 — PUT /usuarios/{id} cria novo usuário ao invés de atualizar

**Endpoint:** `PUT /usuarios/000000000000000000000000`

**Passos para reproduzir:**
1. Enviar uma requisição PUT com um ID que não existe na base
2. Incluir um body válido com nome, email, password e administrador

**Resultado esperado:** `404 Not Found` — o recurso não existe

**Resultado obtido:** `201 Created` — a API ignora o ID da URL e cria um novo usuário com um ID gerado automaticamente

**Severidade:** Alta — uma operação de atualização se comporta como criação silenciosa, podendo gerar registros duplicados sem que o cliente perceba

---

### Bug 2 — DELETE /usuarios/{id} retorna 200 para ID inexistente

**Endpoint:** `DELETE /usuarios/000000000000000000000000`

**Passos para reproduzir:**
1. Enviar uma requisição DELETE com um ID que não existe na base

**Resultado esperado:** `404 Not Found` — o recurso não existe

**Resultado obtido:** `200 OK` com body `{ "message": "Nenhum registro excluído" }`

**Severidade:** Média — não causa perda de dados, mas viola o padrão REST e induz falsa impressão de sucesso em quem consome a API

---

## CI/CD

A suíte é executada automaticamente via GitHub Actions a cada push no repositório.

Consulte `.github/workflows/tests.yml` para ver a configuração do pipeline.

---

## Autor

Andressa Mistura
