import streamlit as st
import pandas as pd

# Função para carregar dados do Excel
def carregar_dados(arquivo):
    return pd.read_excel(arquivo)

# Função para filtrar dados com base no termo de pesquisa
def filtrar_dados(df, coluna, termo):
    # Converter a coluna para string antes de aplicar o filtro
    df[coluna] = df[coluna].astype(str)
    return df[df[coluna] == termo]

# Função para autenticar o usuário
def autenticar(usuario, senha):
    # Defina suas credenciais aqui
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

    # Carregar dados
    df = carregar_dados('resultado.xlsx')  # Substitua pelo nome do seu arquivo Excel

    # Definir o nome da coluna a ser pesquisada
    nome_coluna = 'numero da planilha original'  # Nome da coluna para pesquisa

    # Campo de pesquisa
    termo_pesquisa = st.text_input(f'Digite o número do processo:')

    # Definir as colunas a serem exibidas no resultado
    colunas_a_exibir = ['numero da planilha original', 'alunos']  # Defina as colunas aqui

    # Mostrar resultados se houver termo de pesquisa
    if termo_pesquisa:
        resultados = filtrar_dados(df, nome_coluna, termo_pesquisa)
        if not resultados.empty:
            # Selecionar um item da pesquisa
            item_selecionado = st.selectbox('Selecione um item para ver os detalhes:', resultados.index)
            if item_selecionado is not None:
                st.session_state.selected_item = item_selecionado

            # Botão para ver proposta
            if st.button('Ver Proposta', key='ver_proposta'):
                st.session_state.viewing_proposal = True
        else:
            st.write('Nenhum resultado encontrado.')

# Se estiver logado e um item foi selecionado, exibir os detalhes do item
if st.session_state.logged_in and st.session_state.selected_item is not None and not st.session_state.viewing_proposal:
    st.title('Detalhes do Processo')

    # Carregar dados
    df = carregar_dados('resultado.xlsx')  # Substitua pelo nome do seu arquivo Excel

    # Obter detalhes do item selecionado
    item_detalhes = df.loc[st.session_state.selected_item]
    
    # Exibir detalhes
    st.write('Detalhes do item selecionado:')
    st.write(item_detalhes)

    # Botão para voltar à tela de pesquisa
    if st.button('Voltar', key='voltar_detalhes'):
        st.session_state.selected_item = None

    # Botão para ver proposta
    if st.button('Ver Proposta', key='ver_proposta_detalhes'):
        st.session_state.viewing_proposal = True

# Se estiver vendo a proposta, exibir a nova tela com os 4 campos
if st.session_state.viewing_proposal:
    st.title('Proposta 1')
    # Exibir campos com valores específicos da linha
    st.write("Campo para a proposta 1")  # Substitua 'campo1' pelo nome da coluna desejada
    
    st.title('Proposta 2')
    
    st.write('Campo para a proposta 2')  # Substitua 'campo2' pelo nome da coluna desejada
    
    st.title('Proposta 3')
    
    st.write('Campo para a proposta 3')  # Substitua 'campo3' pelo nome da coluna desejada

    st.title('Proposta Modular')
    # Campo para adicionar um valor para cálculo
    valor_adicional = st.number_input('Digite um valor para o cálculo:', min_value=0, step=1)
    
    st.write('Campo para a proposta 4')  # Substitua 'campo4' pelo nome da coluna desejada
    
    # Campo de entrada para e-mail
    email_input = st.text_input('Digite o e-mail para envio:')
    
    # Botão decorativo para enviar e-mail
    if st.button('Enviar E-mail', key='enviar_email'):
        st.write(f"E-mail a ser enviado para: {email_input}")
        st.write("Botão decorativo para envio de e-mail (a funcionalidade não está implementada).")

    # Botão para voltar para a tela de pesquisa
    if st.button('Voltar para Pesquisa', key='voltar_pesquisa'):
        st.session_state.selected_item = None
        st.session_state.viewing_proposal = False
