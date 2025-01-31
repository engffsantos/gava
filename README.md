# Sistema de Doações

Este projeto é um sistema completo para gerenciar doações, permitindo o controle de pessoas, produtos e as doações realizadas. O sistema foi desenvolvido com o objetivo de simplificar a gestão de recursos em instituições de caridade ou organizações sociais.

---

## 📚 Funcionalidades

### 1. Gerenciamento de Pessoas
- Cadastro de novas pessoas com informações completas, incluindo:
  - Nome
  - Endereço
  - Bairro
  - Telefone
  - Quantidade de filhos
  - Profissão
  - Locomoção
  - Data de cadastro
- Listagem de todas as pessoas cadastradas.

### 2. Gerenciamento de Produtos
- Cadastro de produtos com os seguintes atributos:
  - Nome do produto
  - Descrição
  - Preço
  - Estoque disponível
- Atualização automática do estoque após cada doação.
- Listagem de todos os produtos cadastrados.

### 3. Gerenciamento de Doações
- Registro de doações associando:
  - Pessoa que realizou a doação.
  - Produto doado.
  - Quantidade doada.
  - Data da doação.
- Listagem completa das doações realizadas com informações detalhadas.

### 4. Relatórios
- Geração de relatórios para análise de dados:
  - Pessoas que realizaram doações.
  - Produtos mais doados.
  - Histórico de doações.

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Flask**: Framework web para construção da API e lógica de backend.
- **Flask-SQLAlchemy**: ORM para interagir com o banco de dados.
- **Flask-Migrate**: Gerenciamento de migrações do banco de dados.

### Frontend
- **HTML5**
- **CSS3**
- **Bootstrap 5**

### Banco de Dados
- **MySQL**: Banco de dados relacional para armazenamento das informações.

---

## 🗂️ Estrutura do Projeto

```plaintext
sistema_doacoes/
│
├── app/
│   ├── __init__.py           # Inicializa o aplicativo Flask
│   ├── models/               # Contém os modelos (Model)
│   │   ├── __init__.py
│   │   ├── pessoa.py         # Modelo para tabela 'pessoas'
│   │   ├── produto.py        # Modelo para tabela 'produtos'
│   │   └── doacao.py         # Modelo para tabela 'doacoes'
│   │
│   ├── controllers/          # Contém os controladores (Controller)
│   │   ├── __init__.py
│   │   ├── pessoa_controller.py # CRUD de pessoas e relatórios relacionados
│   │   ├── produto_controller.py # CRUD de produtos e estoque
│   │   └── doacao_controller.py  # Registro de doações e relatórios
│   │
│   ├── templates/            # Contém os templates HTML (View)
│   │   ├── base.html         # Template base
│   │   ├── pessoas/          # Templates relacionados a pessoas
│   │   │   ├── cadastro.html
│   │   │   └── lista.html
│   │   ├── produtos/         # Templates relacionados a produtos
│   │   │   ├── cadastro.html
│   │   │   └── lista.html
│   │   └── doacoes/          # Templates relacionados a doações
│   │       ├── registro.html
│   │       └── relatorio.html
│   │
│   ├── static/               # Arquivos estáticos (CSS, JS, imagens)
│   │   ├── css/
│   │   │   └── style.css     # Estilos customizados
│   │   └── js/
│   │       └── script.js     # Scripts customizados
│   │
│   ├── utils/                # Funções auxiliares e configurações
│   │   ├── __init__.py
│   │   └── db.py             # Conexão ao banco de dados
│   │
│   └── routes.py             # Define as rotas do aplicativo
│
├── instance/
│   └── config.py             # Configurações da aplicação
│
├── migrations/               # Arquivos de migração do banco de dados
│
├── tests/                    # Testes automatizados
│   ├── __init__.py
│   ├── test_pessoa.py        # Testes para 'pessoas'
│   ├── test_produto.py       # Testes para 'produtos'
│   └── test_doacao.py        # Testes para 'doações'
│
├── venv/                     # Ambiente virtual do Python
│
├── .env                      # Variáveis de ambiente (credenciais do BD)
├── .gitignore                # Arquivos a serem ignorados pelo Git
├── requirements.txt          # Dependências do projeto
├── run.py                    # Arquivo principal para executar o app
└── README.md                 # Documentação do projeto
```

---

## ⚙️ Configuração e Execução

### 1. Pré-requisitos
- Python 3.10+
- MySQL
- Ambiente virtual Python (venv)

### 2. Instalação

Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
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

### 3. Configuração do Banco de Dados

Edite o arquivo `instance/config.py` com as credenciais do seu banco MySQL:

```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://usuario:senha@localhost:3306/sistema_doacoes'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### 4. Inicialização do Banco de Dados

Crie as tabelas e aplique as migrações:

```bash
flask db init
flask db migrate -m "Criação inicial das tabelas"
flask db upgrade
```

### 5. Executando o Sistema

Inicie o servidor:

```bash
flask run
```

Acesse o sistema em: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧪 Testes

Para executar os testes automatizados:

```bash
pytest tests/
```

