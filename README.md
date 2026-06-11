# Desafio API - Testes Automatizados (ServeRest)

Este projeto tem como objetivo a prática de automação de testes de API REST utilizando Python, Pytest e Requests, com base na API pública ServeRest.

Os testes validam cenários reais envolvendo usuários, produtos e carrinhos, incluindo fluxos positivos e negativos.

---

## API utilizada

https://compassuol.serverest.dev

---

## Tecnologias utilizadas

- Python 3.10+
- Pytest
- Requests
- UUID

---

## Instalação do projeto

Clone o repositório:

git clone https://github.com/andressamistura2006-max/Desafio-API.git

Entre na pasta do projeto:

cd Desafio-API

Instale as dependências:

pip install -r requirements.txt

---

## Execução dos testes

Executar todos os testes:

pytest -v

Executar com logs detalhados:

pytest -v -s

---

## Estrutura do projeto

O projeto utiliza funções auxiliares para suporte na criação de dados dinâmicos e independência dos testes.

### Funções auxiliares

- gerar_email()
  Gera e-mails únicos utilizando UUID para evitar conflitos entre execuções.

- criar_usuario()
  Cria um usuário automaticamente para ser utilizado em testes que dependem de um usuário existente.

---

## Cenários testados

### Usuários

- Cadastro de usuário com sucesso
- Cadastro com email duplicado
- Cadastro sem email (validação de campo obrigatório)
- Busca de usuário por ID
- Busca de usuário inexistente
- Atualização de usuário
- Exclusão de usuário

---

### Produtos

- Listagem de produtos
- Busca de produto por ID

---

### Carrinhos

- Listagem de carrinhos
- Busca de carrinho por ID

---

## Validações realizadas

Os testes validam:

- Status code das respostas HTTP (200, 201, 400)
- Estrutura do JSON retornado pela API
- Mensagens de sucesso e erro
- Consistência dos dados retornados
- Integridade dos IDs gerados dinamicamente

---

## Estratégia de testes

- Testes independentes entre si
- Uso de dados dinâmicos para evitar conflitos
- Reutilização de usuários criados via função auxiliar
- Cobertura de cenários positivos e negativos
- Validação completa de endpoints REST (CRUD)

---

## Endpoints testados

POST /usuarios  
GET /usuarios/{id}  
PUT /usuarios/{id}  
DELETE /usuarios/{id}  

GET /produtos  
GET /produtos/{id}  

GET /carrinhos  
GET /carrinhos/{id}

---

## Cobertura

- Usuários: CRUD completo
- Produtos: leitura
- Carrinhos: leitura

---

## Observações

Este projeto foi desenvolvido com foco em aprendizado e prática de automação de testes de API.

A estrutura pode ser evoluída para um framework profissional com camadas de service, fixtures e relatórios automatizados.

---

## Autor

Andressa Mistura