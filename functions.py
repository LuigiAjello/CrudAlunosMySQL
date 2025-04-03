from db_connection import engine
from sqlalchemy import text
import streamlit as st
import pandas as pd


def cadastrar_endereco(params: dict):
    """
    Cadastra um novo endereço no banco de dados.

    Args:
        params (dict): Dicionário contendo os parâmetros do endereço:
            - cep (str): CEP do endereço
            - endereco (str): Nome da rua/avenida
            - cidade (str): Cidade do endereço
            - estado (str): Sigla do estado

    Returns:
        None
    """
    sql = text("""
        INSERT INTO tb_enderecos (cep, endereco, cidade, estado)
        VALUES (:cep, :endereco, :cidade, :estado)
    """)
    with engine.begin() as conn:
        conn.execute(sql, params)


def cadastrar_alunos(params: dict):
    """
    Cadastra um novo aluno no banco de dados.

    Args:
        params (dict): Dicionário contendo os parâmetros do aluno:
            - nome_aluno (str): Nome completo do aluno
            - email (str): Email do aluno
            - cep (str): CEP do endereço do aluno
            - carro_id (int): ID do carro associado ao aluno (opcional)

    Returns:
        None
    """
    sql = text("""
        INSERT INTO tb_alunos (nome_aluno, email, cep, carro_id)
        VALUES (:nome_aluno, :email, :cep, :carro_id)
    """)
    with engine.begin() as conn:
        conn.execute(sql, params)


def update_alunos(nome_aluno, novo_nome=None, novo_email=None, novo_cep=None, novo_carro_id=None):
    """
    Atualiza os dados de um aluno existente no banco de dados.

    Args:
        nome_aluno (str): Nome do aluno a ser atualizado
        novo_nome (str, optional): Novo nome para o aluno
        novo_email (str, optional): Novo email para o aluno
        novo_cep (str, optional): Novo CEP para o aluno
        novo_carro_id (int, optional): Novo ID de carro para o aluno

    Returns:
        str: Mensagem indicando o resultado da operação
    """
    aluno_id = get_id_by_nome(nome_aluno)
    
    if not aluno_id:
        return "Aluno não encontrado!"
    
    campos_para_atualizar = []
    params = {"ID": aluno_id}

    if novo_nome:
        campos_para_atualizar.append("nome_aluno = :novo_nome")
        params["novo_nome"] = novo_nome

    if novo_email:
        campos_para_atualizar.append("email = :novo_email")
        params["novo_email"] = novo_email

    if novo_cep:
        campos_para_atualizar.append("cep = :novo_cep")
        params["novo_cep"] = novo_cep

    if novo_carro_id:
        campos_para_atualizar.append("carro_id = :novo_carro_id")
        params["novo_carro_id"] = novo_carro_id

    if not campos_para_atualizar:
        return "Nenhum campo para atualizar."

    sql = text(f"""
        UPDATE tb_alunos
        SET {", ".join(campos_para_atualizar)}
        WHERE id = :ID
    """)

    with engine.begin() as conn:
        conn.execute(sql, params)

    return "Aluno atualizado com sucesso!"


def get_all_alunos():
    """
    Obtém uma lista com os nomes de todos os alunos cadastrados.

    Returns:
        list: Lista de strings com os nomes dos alunos
    """
    sql = text("SELECT nome_aluno FROM tb_alunos")
    with engine.connect() as conn:
        result = conn.execute(sql).fetchall()
    return [aluno[0] for aluno in result]


def get_id_by_nome(nome_aluno):
    """
    Obtém o ID de um aluno a partir do seu nome.

    Args:
        nome_aluno (str): Nome do aluno a ser pesquisado

    Returns:
        int: ID do aluno encontrado ou None se não existir
    """
    sql = text("SELECT id FROM tb_alunos WHERE nome_aluno = :nome_aluno")
    with engine.connect() as conn:
        result = conn.execute(sql, {'nome_aluno': nome_aluno}).fetchone()
    return result[0] if result else None


def get_all_disciplinas():
    """
    Obtém uma lista com os nomes de todas as disciplinas cadastradas.

    Returns:
        list: Lista de strings com os nomes das disciplinas
    """
    sql = text("SELECT nome_disciplina FROM tb_disciplinas")
    with engine.connect() as conn:
        result = conn.execute(sql).fetchall()
    return [disciplina[0] for disciplina in result]


def get_id_by_nome_disciplina(nome_disciplina):
    """
    Obtém o ID de uma disciplina a partir do seu nome.

    Args:
        nome_disciplina (str): Nome da disciplina a ser pesquisada

    Returns:
        int: ID da disciplina encontrada ou None se não existir
    """
    sql = text("SELECT id FROM tb_disciplinas WHERE nome_disciplina = :nome_disciplina")
    with engine.connect() as conn:
        result = conn.execute(sql, {'nome_disciplina': nome_disciplina}).fetchone()
    return result[0] if result else None


def cadastrar_notas(params: dict):
    """
    Cadastra uma nova nota no banco de dados.

    Args:
        params (dict): Dicionário contendo os parâmetros da nota:
            - aluno_id (int): ID do aluno
            - disciplina_id (int): ID da disciplina
            - nota (float): Valor da nota

    Returns:
        None
    """
    sql = text("""
        INSERT INTO tb_notas (aluno_id, disciplina_id, nota)
        VALUES (:aluno_id, :disciplina_id, :nota)
    """)
    with engine.begin() as conn:
        conn.execute(sql, params)


def upload_xls():
    """
    Exibe uma interface para upload de arquivos XLS/XLSX usando Streamlit.

    Returns:
        UploadedFile or None: Objeto do arquivo carregado ou None se nenhum arquivo foi carregado
    """
    st.title("Upload de Arquivo XLS")
    
    # Upload do arquivo
    file = st.file_uploader("Escolha um arquivo XLS", type=["xls", "xlsx"])
    
    if file is not None:
        st.success("Arquivo carregado com sucesso!")
        return file
    else:
        return None


def cadastrar_alunos_xls():
    """
    Cadastra alunos a partir de um arquivo XLS/XLSX.
    
    Lê dados de um arquivo Excel e insere na tabela de alunos.
    Exibe mensagens de erro/sucesso usando Streamlit.
    """
    file = upload_xls()
    if file is not None:
        df_alunos = pd.read_excel(file)
        df_alunos.to_sql('tb_alunos', con=engine, if_exists='append', index=False)
    else:
        st.error("Nenhum arquivo foi carregado ainda.")


def cadastrar_enderecos_xls():
    """
    Cadastra endereços a partir de um arquivo XLS/XLSX.
    
    Lê dados de um arquivo Excel e insere na tabela de endereços.
    Exibe mensagens de erro/sucesso usando Streamlit.
    """
    file = upload_xls()
    if file is not None:
        df_enderecos = pd.read_excel(file)
        df_enderecos.to_sql('tb_enderecos', con=engine, if_exists='append', index=False)
    else:
        st.error("Nenhum arquivo foi carregado ainda.")


def cadastrar_notas_xls():
    """
    Cadastra notas a partir de um arquivo XLS/XLSX.
    
    Lê dados de um arquivo Excel e insere na tabela de notas.
    Exibe mensagens de erro/sucesso usando Streamlit.
    """
    file = upload_xls()
    if file is not None:
        df_notas = pd.read_excel(file)
        df_notas.to_sql('tb_notas', con=engine, if_exists='append', index=False)
    else:
        st.error("Nenhum arquivo foi carregado ainda.")



def get_dados_aluno_relatorio(nome_aluno):
    '''
    Retorna os dados de um aluno pelo nome, incluindo suas notas e disciplinas.
    
    Parametros:
    nome_aluno (str): Nome do aluno.
    
    Retorna:
    dict: Dicionario contendo o nome, email e lista de disciplinas com notas do aluno, ou None se nao encontrado.
    '''
    sql = text("""
        SELECT 
            a.nome_aluno, 
            a.email, 
            d.nome_disciplina, 
            d.carga, 
            d.semestre, 
            n.nota
        FROM tb_alunos a
        JOIN tb_notas n ON a.id = n.aluno_id
        JOIN tb_disciplinas d ON n.disciplina_id = d.id
        WHERE a.nome_aluno = :nome_aluno
    """)
    
    with engine.connect() as conn:
        result = conn.execute(sql, {'nome_aluno': nome_aluno}).fetchall()
    
    if not result:
        return None  # Se a consulta não retornar nenhum resultado, retorna None.

    # Se houver resultado, cria e retorna um dicionário estruturado com os dados do aluno.
    return {
        "nome": result[0][0],  # Nome do aluno, presente na primeira linha e primeira coluna do resultado.
        "email": result[0][1],  # Email do aluno, presente na primeira linha e segunda coluna do resultado.
        "disciplinas": [  # Lista de disciplinas cursadas pelo aluno
            {
                "disciplina": row[2],  # Nome da disciplina
                "carga_horaria": row[3],  # Carga horária da disciplina
                "semestre": row[4],  # Semestre em que a disciplina foi cursada
                "nota": row[5]  # Nota do aluno na disciplina
            }
            for row in result  # Itera sobre todas as linhas retornadas pela consulta para compor a lista de disciplinas
        ]
    }