import streamlit as st
import pandas as pd

# Função para carregar dados do Excel
def carregar_dados(arquivo):
    return pd.read_excel(arquivo)

# Função para filtrar dados com base no termo de pesquisa
def filtrar_dados(df, coluna, termo):
    df[coluna] = df[coluna].astype(str)
    return df[df[coluna] == termo]

# Função para autenticar o usuário
def autenticar(usuario, senha):
    usuario_correto = 'jorge'
    senha_correta = 'jowjow11'
    return usuario == usuario_correto and senha == senha_correta

# Verificar se o usuário está logado
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Verificar se um item foi selecionado para exibir detalhes
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None

# Verificar se está visualizando a proposta
if 'viewing_proposal' not in st.session_state:
    st.session_state.viewing_proposal = False

# Se não estiver logado, exibir a tela de login
if not st.session_state.logged_in:
    st.title('Dashboard - Login')
    
    username = st.text_input('Usuário')
    password = st.text_input('Senha', type='password')

    if st.button('Login'):
        if autenticar(username, password):
            st.session_state.logged_in = True
        else:
            st.error('Usuário ou senha incorretos.')

# Se estiver logado e não houver item selecionado, exibir a tela de pesquisa
if st.session_state.logged_in and st.session_state.selected_item is None and not st.session_state.viewing_proposal:
    st.title('Sistema Jackson Adv. Associados')

    df = carregar_dados('resultado.xlsx')

    nome_coluna = 'numero da planilha original'

    termo_pesquisa = st.text_input(f'Digite o número do processo:')

    colunas_a_exibir = ['numero da planilha original', 'alunos']

    if termo_pesquisa:
        resultados = filtrar_dados(df, nome_coluna, termo_pesquisa)
        if not resultados.empty:
            item_selecionado = st.selectbox('Selecione um item para ver os detalhes:', resultados.index)
            if item_selecionado is not None:
                st.session_state.selected_item = item_selecionado

            if st.button('Ver Proposta', key='ver_proposta'):
                st.session_state.viewing_proposal = True
        else:
            st.write('Nenhum resultado encontrado.')

# Se estiver logado e um item foi selecionado, exibir os detalhes do item
if st.session_state.logged_in and st.session_state.selected_item is not None and not st.session_state.viewing_proposal:
    st.title('Detalhes do Processo')

    df = carregar_dados('resultado.xlsx')

    item_detalhes = df.loc[st.session_state.selected_item]
    
    st.write('Detalhes do item selecionado:')
    st.write(item_detalhes)

    if st.button('Voltar', key='voltar_detalhes'):
        st.session_state.selected_item = None

    if st.button('Ver Proposta', key='ver_proposta_detalhes'):
        st.session_state.viewing_proposal = True

# Se estiver vendo a proposta, exibir a nova tela com os 4 campos
if st.session_state.viewing_proposal:
    st.title('Proposta 1')
    st.write("Campo para a proposta 1")
    
    st.title('Proposta 2')
    st.write('Campo para a proposta 2')
    
    st.title('Proposta 3')
    st.write('Campo para a proposta 3')

    st.title('Proposta Modular')
    valor_adicional = st.number_input('Digite um valor para o cálculo:', min_value=0, step=1)
    
    st.write('Campo para a proposta 4')

    # Campo decorativo com opções de e-mail
    emails = [
        'email1@dominio.com',
        'email2@dominio.com',
        'email3@dominio.com',
        'email4@dominio.com',
        'email5@dominio.com'
    ]
    email_selecionado = st.selectbox('Selecione um e-mail para envio:', emails)
    
    # Botão decorativo para enviar e-mail
    if st.button('Enviar E-mail', key='enviar_email'):
        st.write(f"E-mail selecionado: {email_selecionado}")
        st.write("E-mail enviado com sucesso")

    if st.button('Voltar para Pesquisa', key='voltar_pesquisa'):
        st.session_state.selected_item = None
        st.session_state.viewing_proposal = False
