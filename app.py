import streamlit as st
from functions import cadastrar_endereco, cadastrar_alunos, update_alunos, get_all_alunos, get_id_by_nome, cadastrar_notas, get_all_disciplinas, get_id_by_nome_disciplina
from functions import cadastrar_enderecos_xls, cadastrar_alunos_xls,cadastrar_notas_xls

# Título do aplicativo
st.title("Meu Sistema Escolar")

# Menu lateral
menu = st.sidebar.selectbox("Selecione", ["Cadastrar Endereço", "Cadastrar e atualizar Alunos", "Cadastrar Notas"])






# Se o usuário escolheu "Cadastrar Endereço"
if menu == "Cadastrar Endereço":
    st.subheader("Cadastro de Endereço")
    
    # Inputs do usuário
    cep = st.text_input("Cadastre o CEP")
    endereco = st.text_input("Cadastre o endereço")  
    estado = st.text_input("Cadastre o estado")
    cidade = st.text_input("Cadastre a cidade")

    # Botão para cadastrar
    if st.button("Cadastrar"):
        if cep and endereco and estado and cidade:
            params = {
                'cep': cep,
                'endereco': endereco,
                'estado': estado,
                'cidade': cidade,
            }
            cadastrar_endereco(params)
            st.success("Endereço cadastrado com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos!")

    st.subheader("   OU   ")
    cadastrar_enderecos_xls()






# Se o usuário escolheu "Cadastrar e atualizar Alunos"
if menu == "Cadastrar e atualizar Alunos":
    st.subheader("Cadastro e Atualização de Alunos")

    # Radio button para escolher entre cadastrar ou atualizar
    acao = st.radio("Escolha uma ação", ["Cadastrar Aluno", "Atualizar Aluno"])

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
        cadastrar_alunos_xls()

    # Atualização de aluno
    elif acao == "Atualizar Aluno":
        alunos = get_all_alunos()
        nome_aluno = st.selectbox("Selecione o Aluno que deseja atualizar", alunos)

        # Entradas para atualização
        novo_nome = st.text_input("Novo Nome (opcional)")
        novo_email = st.text_input("Novo Email (opcional)")
        novo_cep = st.text_input("Novo CEP (opcional)")
        novo_carro_id = st.text_input("Novo Carro ID (opcional)")

        if st.button("Atualizar Aluno"):
            if nome_aluno:
                mensagem = update_alunos(nome_aluno, novo_nome, novo_email, novo_cep, novo_carro_id)
                st.success(mensagem)
            else:
                st.error("Por favor, selecione o nome do aluno para atualização!")








# Se o usuário escolheu "Cadastrar Notas"
if menu == "Cadastrar Notas":
    st.subheader("Cadastro de Notas")
    
    # Seleção do aluno
    alunos = get_all_alunos()
    aluno = st.selectbox("Selecione o Aluno:", alunos)
    aluno_id = get_id_by_nome(aluno)

    # Seleção da disciplina
    disciplinas = get_all_disciplinas()
    disciplina = st.selectbox("Selecione a Disciplina:", disciplinas)
    disciplina_id = get_id_by_nome_disciplina(disciplina)

    nota = st.text_input("Nota (0.00)")

    # Botão para cadastrar
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
    cadastrar_notas_xls()