# Sistema Escolar - Gestão de Alunos, Disciplinas e Notas

Um sistema completo para gerenciamento de alunos, disciplinas, notas e geração de relatórios em PDF, desenvolvido com Python, Streamlit, SQLAlchemy e MySQL.

## 📌 Funcionalidades

- **Cadastro de Endereços**: Via formulário ou importação de arquivo XLS/XLSX
- **Gestão de Alunos**: Cadastro, atualização e consulta
- **Gestão de Notas**: Associação de notas a alunos e disciplinas
- **Relatórios**: Geração de PDF com desempenho do aluno (gráfico incluído)
- **Importação de Dados**: Suporte a arquivos Excel para cadastro em massa

## 🛠️ Tecnologias Utilizadas

- **Python** (Linguagem principal)
- **Streamlit** (Interface web)
- **SQLAlchemy** (ORM para banco de dados)
- **MySQL** (Banco de dados)
- **PyMuPDF (fitz)** (Manipulação de PDF)
- **Matplotlib** (Geração de gráficos)
- **pandas** (Manipulação de dados)

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.8+
- MySQL Server
- Git (opcional)

### 🔧 Configuração Inicial

1. **Clone o repositório**:
   ```bash
   git clone    https://github.com/LuigiAjello/CrudAlunosMySQL.git
   cd nome-do-repositorio
   ```
2. **Crie e ative um ambiente virtual (recomendado):** 
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```
3. **Instale as dependências:** 
    ```bash
    pip install -r requirements.txt
    ```
4. **Configure o banco de dados:**

    - Execute o script SQL create_db_escola.sql no seu MySQL

    - Crie um arquivo .env na raiz do projeto com as credenciais:

    ```bash
    DB_HOST=localhost
    DB_PORT=3306
    DB_USER=seu_usuario
    DB_PASSWORD=sua_senha
    DB_NAME=db_escola
    ```
### 💻 Executando a Aplicação
    streamlit run app.py
O sistema estará disponível em: http://localhost:8501

## 📂 Estrutura do Projeto
    .
    ├── app.py                 # Aplicação principal (Streamlit)
    ├── add_pdf.py             # Geração de relatórios PDF
    ├── db_connection.py       # Conexão com o banco de dados
    ├── functions.py           # Funções de negócio e CRUD
    ├── create_db_escola.sql   # Script de criação do banco
    ├── requirements.txt       # Dependências do projeto
    └── .env.example           # Modelo de variáveis de ambiente

## 📝 Como Utilizar

1. Menu Cadastrar Endereço:

    - Preencha os campos ou importe um arquivo Excel

2.  Menu Cadastrar/Atualizar Alunos:

    -  Cadastre novos alunos ou atualize existentes

    - Opção de importação em massa via Excel

3.  Menu Cadastrar Notas:

    - Associe notas a alunos e disciplinas

    - Importação em massa disponível

4.  Menu Relatório Aluno:

    - Selecione um aluno para visualizar dados

    - Gere e baixe um PDF com desempenho completo

## 📄 Exemplo de Arquivo Excel para Importação

Certifique-se que os arquivos Excel seguem estes formatos:

### Alunos:

| nome_aluno   | email    |    cep  | carro_id|
|----------------|--------------|--------------|--------------|
| João Silva  | joao@email.com|01234567	|  1|
| Maria Oliveira | maria@email.com|	98765432|  NULL|
| Carlos Souza | carlos@email.com|45678901|  2|


### Endereços:

| cep   | endereco    |  cidade    | estado|
|----------------|--------------|--------------|--------------|
| 01234567 | Rua das Flores, 100	|São Paulo		| SP|
| 98765432  | Avenida Brasil, 2000|	Rio de Janeiro|  RJ|
| 45678901  | Praça da Sé, 1	|São Paulo	|  SP|


### Notas:

| aluno_id   | disciplina_id    |  nota    |
|----------------|--------------|--------------|
| 1 | 1	| 8.5		|
| 1  | 3|	7.0|  
| 2  | 2|9.2|  
|3  | 1|6.8| 

## 🤝 Contribuição
Contribuições são bem-vindas! Siga estes passos:

1. Faça um fork do projeto

2. Crie uma branch (git checkout -b feature/nova-feature)

3. Commit suas mudanças (git commit -m 'Adiciona nova feature')

4. Push para a branch (git push origin feature/nova-feature)

5. Abra um Pull Request
