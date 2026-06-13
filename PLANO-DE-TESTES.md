# Plano de Testes - Desafio API ServeRest

## 1. Objetivo

Validar o comportamento dos principais endpoints da API ServeRest, cobrindo fluxos positivos e negativos. A suite testa a API diretamente via HTTP, desde cadastro e login ate operacoes com produtos e leitura de carrinhos.

A suite foi construida de forma incremental: primeiro em um arquivo unico legado (`test_desafio_api.py`) e depois em uma estrutura modular por dominio (`tests/` + `helpers/`).

---

## 2. Estrategia

| Item | Decisao |
|---|---|
| Tipo de teste | Testes de API, caixa-preta, nivel de integracao |
| Ferramenta principal | Python + Pytest + Requests |
| Geracao de dados | UUID para e-mails e nomes unicos |
| Autenticacao | Fixture de sessao `token_admin` |
| Execucao oficial | `pytest` ou `pytest tests/ -v` |
| Arquivo legado | `test_desafio_api.py`, fora da coleta padrao pelo `pytest.ini` |

Cada teste cria seus proprios dados quando necessario, reduzindo dependencia entre cenarios. Os testes que exigem autenticacao reutilizam um token de administrador criado pela fixture de sessao.

---

## 3. Escopo

### Dentro do escopo

| Endpoint | Operacoes cobertas |
|---|---|
| `POST /usuarios` | Cadastro com sucesso, email duplicado, campo obrigatorio ausente |
| `GET /usuarios/{id}` | Busca por ID existente e inexistente |
| `PUT /usuarios/{id}` | Atualizacao de dados |
| `DELETE /usuarios/{id}` | Exclusao com sucesso |
| `POST /login` | Credenciais corretas, senha errada, email inexistente, campos vazios/ausentes |
| `GET /produtos` | Listagem |
| `GET /produtos/{id}` | Busca por ID existente e inexistente |
| `POST /produtos` | Cadastro com token de admin, cadastro sem token |
| `PUT /produtos/{id}` | Atualizacao com token de admin |
| `DELETE /produtos/{id}` | Exclusao com token de admin |
| `GET /carrinhos` | Listagem |
| `GET /carrinhos/{id}` | Busca por ID existente |

### Fora do escopo

| Endpoint | Motivo |
|---|---|
| `POST /carrinhos` | Exige usuario autenticado, produto existente e payload encadeado. Priorizado para proxima iteracao. |
| `DELETE /carrinhos/concluir-compra` | Depende de carrinho ativo criado previamente. |
| `DELETE /carrinhos/cancelar-compra` | Depende de carrinho ativo criado previamente. |
| Testes de carga/performance | Fora do objetivo desta suite. |
| Contratos JSON Schema completos | Fora do escopo atual. |

---

## 4. Cenarios implementados

### Usuarios (`tests/test_usuarios.py`)

| ID | Cenario | Tipo | Status |
|---|---|---|---|
| U01 | Cadastrar usuario com dados validos | Positivo | Implementado |
| U02 | Buscar usuario por ID existente | Positivo | Implementado |
| U03 | Editar usuario com dados validos | Positivo | Implementado |
| U04 | Excluir usuario existente | Positivo | Implementado |
| U05 | Cadastrar usuario com email duplicado | Negativo | Implementado |
| U06 | Cadastrar usuario sem campo email | Negativo | Implementado |
| U07 | Buscar usuario com ID inexistente | Negativo | Implementado |

### Login (`tests/test_login.py`)

| ID | Cenario | Tipo | Status |
|---|---|---|---|
| L01 | Login com credenciais corretas | Positivo | Implementado |
| L02 | Login com senha errada | Negativo | Implementado |
| L03 | Login com email inexistente | Negativo | Implementado |
| L04 | Login sem campo email | Negativo | Implementado |
| L05 | Login sem campo senha | Negativo | Implementado |
| L06 | Login com campos vazios | Negativo | Implementado |

### Produtos (`tests/test_produtos.py`)

| ID | Cenario | Tipo | Status |
|---|---|---|---|
| P01 | Listar produtos | Positivo | Implementado |
| P02 | Buscar produto por ID existente | Positivo | Implementado |
| P03 | Cadastrar produto com token de admin | Positivo | Implementado |
| P04 | Editar produto com token de admin | Positivo | Implementado |
| P05 | Excluir produto com token de admin | Positivo | Implementado |
| P06 | Cadastrar produto sem token | Negativo | Implementado |
| P07 | Buscar produto com ID inexistente | Negativo | Implementado |

### Carrinhos (`tests/test_carrinhos.py`)

| ID | Cenario | Tipo | Status |
|---|---|---|---|
| C01 | Listar carrinhos | Positivo | Implementado |
| C02 | Buscar carrinho por ID existente | Positivo | Implementado |

---

## 5. Criterios de qualidade

Um teste e considerado pronto quando:

- Valida o status code HTTP esperado.
- Valida pelo menos um campo relevante do corpo da resposta.
- E independente de outros testes.
- Usa dados dinamicos quando existe risco de conflito.
- Tem nome descritivo.
- Passa de forma consistente contra a API remota.

---

## 6. Ambiente

| Item | Valor |
|---|---|
| API base URL | `https://compassuol.serverest.dev` |
| Linguagem | Python 3.10+ |
| Framework de testes | Pytest 9.x |
| Biblioteca HTTP | Requests 2.x |
| CI/CD | GitHub Actions |

---

## 7. Riscos e observacoes

- A API remota pode apresentar instabilidade, latencia ou indisponibilidade temporaria.
- O token JWT expira em aproximadamente 10 minutos. Para o escopo atual, a fixture de sessao atende bem, mas em suites maiores vale considerar renovacao automatica.
- O teste de carrinho por ID cria seus proprios dados (usuario, produto e carrinho) para garantir independencia total, sem depender de dados existentes na API publica.
- O arquivo `test_desafio_api.py` preserva os testes da Semana 3 em sua forma original. A execucao oficial da suite fica em `tests/`, configurada pelo `pytest.ini`.
