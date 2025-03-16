from db_connection import engine
from sqlalchemy import text
import streamlit as st
import pandas as pd

# Função para cadastrar endereço
def cadastrar_endereco(params: dict):
    sql = text("""
        INSERT INTO tb_enderecos (cep, endereco, cidade, estado)
        VALUES (:cep, :endereco, :cidade, :estado)
    """)
    with engine.begin() as conn:
        conn.execute(sql, params)



# Função para cadastrar alunos
def cadastrar_alunos(params: dict):
    sql = text("""
        INSERT INTO tb_alunos (nome_aluno, email, cep, carro_id)
        VALUES (:nome_aluno, :email, :cep, :carro_id)
    """)
    with engine.begin() as conn:
        conn.execute(sql, params)




# Função para atualizar aluno pelo nome
def update_alunos(nome_aluno, novo_nome=None, novo_email=None, novo_cep=None, novo_carro_id=None):
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






# Função para obter todos os nomes dos alunos
def get_all_alunos():
    sql = text("SELECT nome_aluno FROM tb_alunos")
    with engine.connect() as conn:
        result = conn.execute(sql).fetchall()
    return [aluno[0] for aluno in result]




# Função para obter o ID pelo nome do aluno
def get_id_by_nome(nome_aluno):
    sql = text("SELECT id FROM tb_alunos WHERE nome_aluno = :nome_aluno")
    with engine.connect() as conn:
        result = conn.execute(sql, {'nome_aluno': nome_aluno}).fetchone()
    return result[0] if result else None




# Função para obter todos os nomes das disciplinas
def get_all_disciplinas():
    sql = text("SELECT nome_disciplina FROM tb_disciplinas")
    with engine.connect() as conn:
        result = conn.execute(sql).fetchall()
    return [disciplina[0] for disciplina in result]




# Função para obter o ID pelo nome da disciplina
def get_id_by_nome_disciplina(nome_disciplina):
    sql = text("SELECT id FROM tb_disciplinas WHERE nome_disciplina = :nome_disciplina")
    with engine.connect() as conn:
        result = conn.execute(sql, {'nome_disciplina': nome_disciplina}).fetchone()
    return result[0] if result else None




# Função para cadastrar notas
def cadastrar_notas(params: dict):
    sql = text("""
        INSERT INTO tb_notas (aluno_id, disciplina_id, nota)
        VALUES (:aluno_id, :disciplina_id, :nota)
    """)
    with engine.begin() as conn:
        conn.execute(sql, params)






def upload_xls():
    st.title("Upload de Arquivo XLS")
    
    # Upload do arquivo
    file = st.file_uploader("Escolha um arquivo XLS", type=["xls", "xlsx"])
    
    if file is not None:
        st.success("Arquivo carregado com sucesso!")
        return file
    else:
        return None







def cadastrar_alunos_xls():
    file = upload_xls()
    if file is not None:
        df_alunos = pd.read_excel(file)
        df_alunos.to_sql('tb_alunos', con=engine, if_exists='append', index=False)
    else:
        st.error("Nenhum arquivo foi carregado ainda.")
    


def cadastrar_enderecos_xls():
    file = upload_xls()
    if file is not None:
        df_enderecos = pd.read_excel(file)
        df_enderecos.to_sql('tb_enderecos', con=engine, if_exists='append', index=False)
    else:
        st.error("Nenhum arquivo foi carregado ainda.")



def cadastrar_notas_xls():
    file = upload_xls()
    if file is not None:

        df_notas = pd.read_excel(file)
        df_notas.to_sql('tb_notas', con=engine, if_exists='append', index=False)
    else:
        st.error("Nenhum arquivo foi carregado ainda.")


