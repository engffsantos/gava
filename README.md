# 📌 Sistema de Doações

## 📖 Descrição
O **Sistema de Doações** é uma aplicação desenvolvida para gerenciar doações de forma eficiente, permitindo o controle de pessoas, produtos e doações realizadas. O objetivo é simplificar a gestão de recursos em instituições de caridade e organizações sociais.

## 🚀 Funcionalidades
### 1️⃣ Gerenciamento de Pessoas
- Cadastro de pessoas com informações detalhadas:
  - Nome
  - Endereço, bairro e telefone
  - Quantidade de filhos
  - Profissão
  - Locomoção
  - Data de cadastro
- Listagem de todas as pessoas cadastradas
- Visualização de doações realizadas e pedidos de doação
- Impede a duplicação de cadastros

### 2️⃣ Gerenciamento de Produtos
- Cadastro de produtos com os atributos:
  - Nome, descrição e estoque disponível
  - Atualização automática do estoque após cada doação
  - Bloqueia doação de produtos sem estoque, exibindo uma mensagem de erro
- Listagem completa dos produtos cadastrados

### 3️⃣ Gerenciamento de Doações
- Registro de doações associando:
  - Pessoa que realizou a doação
  - Produto doado
  - Quantidade doada
  - Data da doação
- Listagem completa das doações realizadas com informações detalhadas

### 4️⃣ Relatórios e Exportação
- Geração de relatórios personalizados:
  - Pessoas que realizaram doações
  - Produtos mais doados
  - Histórico completo de doações
- Exportação de relatórios em PDF
- Sinalização de pedidos já realizados na lista de doações
- Filtragem avançada nos registros

## 🛠️ Tecnologias Utilizadas
### Backend
- Python (Flask)
- SQLite

### Frontend
- HTML5, CSS3 e JavaScript
- Bootstrap

### Banco de Dados
- SQLite

## 📂 Estrutura do Projeto
```
├── 📄 .env
├── 📄 .gitignore
├── 📄 app.py
├── 📄 create_tables.py
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 run.py
├── 📄 vercel.json
├── 📂 app
│   ├── 📄 database.db
│   ├── 📄 routes.py
│   ├── 📄 templates.zip
│   ├── 📄 __init__.py
│   ├── 📂 controllers
│   │   ├── 📄 doacao_controller.py
│   │   ├── 📄 pedido_doacao_controller.py
│   │   ├── 📄 pessoa_controller.py
│   │   ├── 📄 produto_controller.py
│   │   ├── 📄 __init__.py
│   ├── 📂 models
│   │   ├── 📄 doacao.py
│   │   ├── 📄 pedido_doacao.py
│   │   ├── 📄 pessoa.py
│   │   ├── 📄 produto.py
│   │   ├── 📄 __init__.py
│   ├── 📂 static
│   │   ├── 📂 css
│   │   │   ├── 📄 style.css
│   │   ├── 📂 js
│   │   │   ├── 📄 script.js
│   ├── 📂 templates
│   │   ├── 📄 base.html
│   │   ├── 📄 index.html
│   │   ├── 📂 doacoes
│   │   │   ├── 📄 registro.html
│   │   │   ├── 📄 relatorio.html
│   │   ├── 📂 pedidos
│   │   │   ├── 📄 cadastro.html
│   │   │   ├── 📄 exibir_relatorio.html
│   │   │   ├── 📄 lista.html
│   │   │   ├── 📄 relatorio_pedidos.html
│   │   ├── 📂 pessoas
│   │   │   ├── 📄 cadastro.html
│   │   │   ├── 📄 editar.html
│   │   │   ├── 📄 lista.html
│   │   ├── 📂 produtos
│   │   │   ├── 📄 cadastro.html
│   │   │   ├── 📄 editar.html
│   │   │   ├── 📄 lista.html
│   ├── 📂 utils
│   │   ├── 📄 db.py
├── 📂 instance
│   ├── 📄 config.py
├── 📂 migrations
│   ├── 📄 alembic.ini
│   ├── 📄 env.py
│   ├── 📄 README
│   ├── 📄 script.py.mako
│   ├── 📂 versions
├── 📂 tests
│   ├── 📄 test_doacao.py
│   ├── 📄 test_pessoa.py
│   ├── 📄 test_produto.py
│   ├── 📄 __init__.py
```

## ⚙️ Configuração e Execução
### 📌 1. Requisitos
- Python 3.10+
- SQLite
- Ambiente virtual Python (venv)

### 🔧 2. Instalação
Clone o repositório:
```bash
git clone https://github.com/engffsantos/gava.git
cd sistema_doacoes
```
Crie um ambiente virtual e ative-o:
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```
Instale as dependências:
```bash
pip install -r requirements.txt
```

### 🗄️ 3. Inicialização do Banco de Dados
```bash
flask db init
flask db migrate -m "Criação inicial das tabelas"
flask db upgrade
```

### ▶️ 4. Executando o Sistema
```bash
flask run
```
Acesse o sistema em: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🧪 Testes Automatizados
Para rodar os testes:
```bash
pytest tests/
```

## 📄 Licença
Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.


