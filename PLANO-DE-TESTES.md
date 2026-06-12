# Plano de Testes — Desafio API ServeRest

## 1. Objetivo

Validar o comportamento dos principais endpoints da API ServeRest, cobrindo tanto os fluxos que devem funcionar quanto os que devem retornar erro. A ideia é garantir que a API se comporta como esperado em situações reais de uso — desde um cadastro simples até tentativas com dados inválidos ou sem autenticação.

A suíte foi construída de forma incremental, partindo dos testes da Semana 3 e evoluindo para uma estrutura mais organizada, com separação por domínio e cobertura mensurável.

---

## 2. Estratégia

A suíte cobre a camada de API diretamente via HTTP, sem simulação de interface ou mock de serviço. Cada teste cria seus próprios dados usando UUID para evitar conflitos entre execuções, e nenhum teste depende do resultado de outro.

A autenticação é feita uma única vez por sessão através de uma fixture do Pytest, que cria um usuário admin, faz login e distribui o token para todos os testes que precisam dele.

| Item | Decisão |
|---|---|
| Tipo de teste | Testes de API (caixa-preta, nível de integração) |
| Ferramenta principal | Python + Pytest + Requests |
| Geração de dados | UUID para e-mails e nomes únicos por execução |
| Autenticação | Fixture de sessão (`token_admin`) — login feito uma vez, token reutilizado |
| Execução | `pytest tests/ -v` — local e via GitHub Actions a cada push |

---

## 3. Escopo

### Dentro do escopo

| Endpoint | Operações cobertas |
|---|---|
| `POST /usuarios` | Cadastro com sucesso, email duplicado, campo obrigatório ausente |
| `GET /usuarios/{id}` | Busca por ID existente e inexistente |
| `PUT /usuarios/{id}` | Atualização de dados |
| `DELETE /usuarios/{id}` | Exclusão com sucesso |
| `POST /login` | Credenciais corretas, senha errada, email inexistente, campos vazios/ausentes |
| `GET /produtos` | Listagem |
| `GET /produtos/{id}` | Busca por ID existente e inexistente |
| `POST /produtos` | Cadastro com token de admin, cadastro sem token |
| `PUT /produtos/{id}` | Atualização com token de admin |
| `DELETE /produtos/{id}` | Exclusão com token de admin |
| `GET /carrinhos` | Listagem |
| `GET /carrinhos/{id}` | Busca por ID existente |

### Fora do escopo (justificativa)

| Endpoint | Motivo da exclusão |
|---|---|
| `POST /carrinhos` | Exige produto e usuário com token — complexidade de setup alta; priorizado para próxima iteração |
| `DELETE /carrinhos/concluir-compra` | Depende de carrinho ativo; fora do escopo desta sprint |
| `DELETE /carrinhos/cancelar-compra` | Mesma razão acima |
| Testes de carga / performance | Fora do objetivo desta suíte |
| Testes de contrato (schema completo) | Parcialmente coberto via Extra 1 (JSON Schema em 3 endpoints) |

---

## 4. Cenários a implementar

### Usuários (`tests/test_usuarios.py`)

| # | Cenário | Tipo | Status |
|---|---|---|---|
| U01 | Cadastrar usuário com dados válidos | Positivo | ✅ Implementado |
| U02 | Buscar usuário por ID existente | Positivo | ✅ Implementado |
| U03 | Editar usuário com dados válidos | Positivo | ✅ Implementado |
| U04 | Excluir usuário existente | Positivo | ✅ Implementado |
| U05 | Cadastrar usuário com email duplicado | Negativo | ✅ Implementado |
| U06 | Cadastrar usuário sem campo email | Negativo | ✅ Implementado |
| U07 | Buscar usuário com ID inexistente | Negativo | ✅ Implementado |

### Login (`tests/test_login.py`)

| # | Cenário | Tipo | Status |
|---|---|---|---|
| L01 | Login com credenciais corretas | Positivo | ✅ Implementado |
| L02 | Login com senha errada | Negativo | ✅ Implementado |
| L03 | Login com email inexistente | Negativo | ✅ Implementado |
| L04 | Login sem campo email | Negativo | ✅ Implementado |
| L05 | Login sem campo senha | Negativo | ✅ Implementado |
| L06 | Login com campos vazios | Negativo | ✅ Implementado |

### Produtos (`tests/test_produtos.py`)

| # | Cenário | Tipo | Status |
|---|---|---|---|
| P01 | Listar produtos | Positivo | ✅ Implementado |
| P02 | Buscar produto por ID existente | Positivo | ✅ Implementado |
| P03 | Cadastrar produto com token de admin | Positivo | ✅ Implementado |
| P04 | Editar produto com token de admin | Positivo | ✅ Implementado |
| P05 | Excluir produto com token de admin | Positivo | ✅ Implementado |
| P06 | Cadastrar produto sem token | Negativo | ✅ Implementado |
| P07 | Buscar produto com ID inexistente | Negativo | ✅ Implementado |

### Carrinhos (`tests/test_carrinhos.py`)

| # | Cenário | Tipo | Status |
|---|---|---|---|
| C01 | Listar carrinhos | Positivo | ✅ Implementado |
| C02 | Buscar carrinho por ID existente | Positivo | ✅ Implementado |

---

## 5. Critérios de qualidade

Um teste é considerado **pronto** quando atende a todos os critérios abaixo:

- [ ] Valida o **status code** HTTP esperado
- [ ] Valida ao menos um campo relevante do **corpo da resposta** (message, _id, ou campo de dados)
- [ ] É **independente** — não depende de outro teste para passar
- [ ] Usa **dados dinâmicos** (UUID) para evitar conflito entre execuções
- [ ] Tem nome descritivo que identifica o cenário sem precisar ler o corpo
- [ ] Passa de forma consistente em pelo menos **3 execuções consecutivas**

---

## 6. Ambiente

| Item | Valor |
|---|---|
| API base URL | `https://compassuol.serverest.dev` |
| Linguagem | Python 3.10+ |
| Framework de testes | Pytest 9.x |
| Biblioteca HTTP | Requests 2.x |
| CI/CD | GitHub Actions (push em qualquer branch) |

---

## 7. Riscos e observações

- A API remota apresenta **instabilidade esporádica** (503 em `/produtos` e latência no login pós-cadastro). Os testes de login usam `time.sleep(2)` e retry para mitigar esse comportamento.
- O token JWT expira em **10 minutos**. A fixture `token_admin` tem escopo `session`, portanto suítes longas podem expirar o token. Em suítes grandes, considerar escopo `function` ou renovação automática.
- Comportamento de **upsert no PUT `/usuarios`**: a API retorna `201` quando o ID não existe (cria novo registro) e `200` quando atualiza. Isso é um comportamento não-convencional documentado como possível bug.
