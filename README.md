# Sistema de Doações

## 📌 Descrição
Sistema de Doações é um sistema completo para gerenciar doações, permitindo o controle de pessoas, produtos e doações realizadas. O sistema foi desenvolvido com o objetivo de simplificar a gestão de recursos em instituições de caridade ou organizações sociais.

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
- Visualização de doações efetuadas e pedidos de doação.
- Impede a duplicação de cadastros.

### 2. Gerenciamento de Produtos
- Cadastro de produtos com os seguintes atributos:
  - Nome do produto
  - Descrição
  - Preço
  - Estoque disponível
- Atualização automática do estoque após cada doação.
- Listagem de todos os produtos cadastrados.
- Impede a doação de produtos com estoque zerado, exibindo mensagem de erro.

### 3. Gerenciamento de Doações
- Registro de doações associando:
  - Pessoa que realizou a doação.
  - Produto doado.
  - Quantidade doada.
  - Data da doação.
- Listagem completa das doações realizadas com informações detalhadas.

### 4. Relatórios e Exportação
- Geração de relatórios para análise de dados:
  - Pessoas que realizaram doações.
  - Produtos mais doados.
  - Histórico de doações.
- Relatório de doações recebidas por pessoa.
- Sinalização de pedidos já realizados na lista de pedidos de doação.
- Filtragem avançada nas listas de doações.
- Geração de relatórios em PDF com pedidos de doação por cliente.

## 🛠️ Tecnologias Utilizadas
### Backend
- Python (Flask)
- SQLite

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap

### Banco de Dados
- SQLite

## 🗂️ Estrutura do Projeto
```
sistema_doacoes/
│
├── app/
│   ├── __init__.py           # Inicializa o aplicativo Flask
│   ├── models/               # Contém os modelos de dados
│   │   ├── pessoa.py         # Modelo para tabela 'pessoas'
│   │   ├── produto.py        # Modelo para tabela 'produtos'
│   │   └── doacao.py         # Modelo para tabela 'doacoes'
│   │
│   ├── controllers/          # Contém os controladores (Controller)
│   │   ├── pessoa_controller.py # CRUD de pessoas e relatórios
│   │   ├── produto_controller.py # CRUD de produtos e estoque
│   │   └── doacao_controller.py  # Registro de doações e relatórios
│   │
│   ├── templates/            # Contém os templates HTML
│   ├── static/               # Arquivos estáticos (CSS, JS, imagens)
│   ├── utils/                # Funções auxiliares
│   └── routes.py             # Define as rotas do aplicativo
│
├── instance/
│   └── config.py             # Configurações da aplicação
│
├── migrations/               # Arquivos de migração do banco de dados
├── tests/                    # Testes automatizados
├── .env                      # Variáveis de ambiente
├── .gitignore                # Arquivos ignorados pelo Git
├── requirements.txt          # Dependências do projeto
├── run.py                    # Arquivo principal para executar o app
└── README.md                 # Documentação do projeto
```

## ⚙️ Configuração e Execução
### 1. Pré-requisitos
- Python 3.10+
- SQLite
- Ambiente virtual Python (venv)

### 2. Instalação
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

### 3. Inicialização do Banco de Dados
```bash
flask db init
flask db migrate -m "Criação inicial das tabelas"
flask db upgrade
```

### 4. Executando o Sistema
```bash
flask run
```
Acesse o sistema em: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🧪 Testes
Para executar os testes automatizados:
```bash
pytest tests/
```

## 📄 Licença
Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.

