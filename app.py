import streamlit as st
import pandas as pd
from functions import (
    cadastrar_endereco, cadastrar_alunos, update_alunos, get_all_alunos, get_id_by_nome, 
    cadastrar_notas, get_all_disciplinas, get_id_by_nome_disciplina, get_dados_aluno_relatorio,
    cadastrar_enderecos_xls, cadastrar_alunos_xls, cadastrar_notas_xls
)
from add_pdf import gerar_relatorio_pdf

# Titulo do aplicativo
st.title("Meu Sistema Escolar")

# Menu lateral
menu = st.sidebar.selectbox("Selecione", ["Cadastrar Endereco", "Cadastrar e atualizar Alunos", "Cadastrar Notas", "Relatorio Aluno"])

# Se o usuario escolheu "Cadastrar Endereco"
if menu == "Cadastrar Endereco":
    st.subheader("Cadastro de Endereco")
    
    # Inputs do usuario
    cep = st.text_input("Cadastre o CEP")
    endereco = st.text_input("Cadastre o endereco")  
    estado = st.text_input("Cadastre o estado")
    cidade = st.text_input("Cadastre a cidade")

    # Botao para cadastrar
    if st.button("Cadastrar"):
        if cep and endereco and estado and cidade:
            params = {
                'cep': cep,
                'endereco': endereco,
                'estado': estado,
                'cidade': cidade,
            }
            cadastrar_endereco(params)
            st.success("Endereco cadastrado com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos!")

    st.subheader("OU")
    # Opcao de cadastrar via arquivo XLS
    cadastrar_enderecos_xls()



########################################################################################################################################################################



# Se o usuario escolheu "Cadastrar e atualizar Alunos"
if menu == "Cadastrar e atualizar Alunos":
    st.subheader("Cadastro e Atualizacao de Alunos")

    # Radio button para escolher entre cadastrar ou atualizar
    acao = st.radio("Escolha uma acao", ["Cadastrar Aluno", "Atualizar Aluno"])

    # Cadastro de aluno
    if acao == "Cadastrar Aluno":
        nome_aluno = st.text_input("Cadastre o Nome")
        email = st.text_input("Cadastre o email")  
        cep = st.text_input("Cadastre o CEP")
        carro_id = st.text_input("Cadastre o Carro ID")

        if st.button("Cadastrar"):
            if nome_aluno and email and cep and carro_id:
                params = {
                    'nome_aluno': nome_aluno,
                    'email': email,
                    'cep': cep,
                    'carro_id': carro_id,
                }
                cadastrar_alunos(params)  
                st.success("Aluno cadastrado com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos!")
        
        st.subheader("OU")
        # Opcao de cadastrar via arquivo XLS
        cadastrar_alunos_xls()

    # Atualizacao de aluno
    elif acao == "Atualizar Aluno":
        alunos = get_all_alunos()
        nome_aluno = st.selectbox("Selecione o Aluno que deseja atualizar", alunos)

        # Entradas para atualizacao
        novo_nome = st.text_input("Novo Nome (opcional)")
        novo_email = st.text_input("Novo Email (opcional)")
        novo_cep = st.text_input("Novo CEP (opcional)")
        novo_carro_id = st.text_input("Novo Carro ID (opcional)")

        if st.button("Atualizar Aluno"):
            if nome_aluno:
                mensagem = update_alunos(nome_aluno, novo_nome, novo_email, novo_cep, novo_carro_id)
                st.success(mensagem)
            else:
                st.error("Por favor, selecione o nome do aluno para atualizacao!")



########################################################################################################################################################################



# Se o usuario escolheu "Cadastrar Notas"
if menu == "Cadastrar Notas":
    st.subheader("Cadastro de Notas")
    
    # Selecao do aluno
    alunos = get_all_alunos()
    aluno = st.selectbox("Selecione o Aluno:", alunos)
    aluno_id = get_id_by_nome(aluno)

    # Selecao da disciplina
    disciplinas = get_all_disciplinas()
    disciplina = st.selectbox("Selecione a Disciplina:", disciplinas)
    disciplina_id = get_id_by_nome_disciplina(disciplina)

    nota = st.text_input("Nota (0.00)")

    # Botao para cadastrar nota
    if st.button("Cadastrar"):
        if aluno_id and disciplina_id and nota:
            params = {
                'aluno_id': aluno_id,
                'disciplina_id': disciplina_id,
                'nota': nota,
            }
            cadastrar_notas(params)
            st.success("Nota cadastrada com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos!")
    
    st.subheader("OU")
    # Opcao de cadastrar notas via arquivo XLS
    cadastrar_notas_xls()



########################################################################################################################################################################



# Se o usuario escolheu "Relatorio Aluno"
if menu == "Relatorio Aluno":
    st.subheader("Relatorio do Aluno")
    
    # Selecao do aluno para gerar o relatorio
    alunos = get_all_alunos()
    aluno_selecionado = st.selectbox("Selecione o Aluno:", alunos)
    
    if aluno_selecionado:
        dados_aluno = get_dados_aluno_relatorio(aluno_selecionado)
        
        if dados_aluno:
            # Exibir informacoes do aluno
            st.write(f"**Nome:** {dados_aluno['nome']}")
            st.write(f"**Email:** {dados_aluno['email']}")

            # Criar tabela das disciplinas e notas
            df_disciplinas = pd.DataFrame(dados_aluno["disciplinas"])
            st.table(df_disciplinas)

            # Botao para gerar o PDF do relatorio
            if st.button("Baixar Relatorio"):
                caminho_pdf = "relatorio_final.pdf"
                gerar_relatorio_pdf("pdf_relatorio_em_branco.pdf", caminho_pdf, dados_aluno)
                
                with open(caminho_pdf, "rb") as file:
                    st.download_button("Clique aqui para baixar o relatorio", file, file_name="relatorio.pdf", mime="application/pdf")
        else:
            st.error("Nenhum dado encontrado para esse aluno.")
