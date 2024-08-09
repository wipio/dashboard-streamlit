import pandas as pd
import streamlit as st
import os

# Carregar os dados
caminho = os.getcwd()
arquivo = pd.read_excel(os.path.join(caminho, 'nova.xlsx'))
indice = pd.read_excel(os.path.join(caminho, 'indice.xlsx'))

# Funções fornecidas pelo usuário
def dias_em_atraso(vencimento):
    dia_hoje = pd.to_datetime('today')
    dias_atraso = (dia_hoje - vencimento).days
    if dias_atraso < 0:
        dias_atraso = 0
    return dias_atraso

def multa_1_porcento_mes(data_inicio, valor):
    hoje_formatado = pd.to_datetime('today')
    dias_atraso = (hoje_formatado - data_inicio).days
    porcentagem = 1 / 30
    porcentagem_dias = dias_atraso * porcentagem
    valor_multa = (valor * porcentagem_dias) / 100
    return valor_multa    

def multa_20_porcento(valor):
    return valor * 1.20

def multa_2_porcento(valor):
    return valor * 0.02

def formatar_data(data):
    data_atualizada = pd.to_datetime(data)
    return f'{data_atualizada.month}-{data_atualizada.year}'

def buscar_indice(data_formatada, df_indice):
    ind_mes_div = df_indice[df_indice['data abreviada'] == data_formatada]
    return float(ind_mes_div['indice'].values[0])

def obter_indice_mes_atual(df_indice):
    hoje_formatado = f'{pd.Timestamp.today().month}-{pd.Timestamp.today().year}'
    try:
        indice_mes_atual = df_indice[df_indice['data abreviada'] == hoje_formatado]
        return float(indice_mes_atual['indice'].values[0])
    except:
        mes, ano = map(int, hoje_formatado.split('-'))
        if mes == 1:
            mes, ano = 12, ano - 1
        else:
            mes -= 1
        nova_data = f'{mes}-{ano}'
        indice_mes_atual = df_indice[df_indice['data abreviada'] == nova_data]
        return float(indice_mes_atual['indice'].values[0])

def valor_corr_infl(valor_div, indi_mes_div, indi_mes_atual):
    indice_att = 94.458606 / indi_mes_div
    return valor_div * indice_att

def lista_menu(indice):
    linha = arquivo[arquivo['numero da planilha original'] == indice]
    lista_data = (linha['datas att'].values[0]).split(',')
    lista_valores = (linha['valor nominal'].values[0]).split(',')
    aluno = linha['alunos'].values[0]
    return lista_data, lista_valores, aluno

def calcular_propostas(sub_total_divida):
    propostas = {
        '10% de desconto': round(sub_total_divida * 0.90, 2),
        '5% de desconto': round(sub_total_divida * 0.95, 2),
        '5% sem desconto': round(sub_total_divida * 1.05, 2),
        '10% sem desconto': round(sub_total_divida * 1.10, 2),
    }
    return propostas

# Interface com Streamlit
st.sidebar.title('Navegação')
page = st.sidebar.radio('Escolha uma página:', ['Consulta de Processos', 'Propostas'])

if page == 'Consulta de Processos':
    st.title('Consulta de Processos')

    # Input do número do processo
    numero_processo = st.text_input('Número do Processo')

    if st.button('Consultar'):
        if numero_processo.isdigit():
            numero_processo = int(numero_processo)
            datas, lista_valores,aluno = lista_menu(numero_processo)

            lista_valores_att_infl = []
            lista_valores_multa_1p = []
            lista_valores_multa_2p = []
            lista_valor_soma_mes = []
            sub_total_divida = ''
            valor_somado_divida = ''

            for num_linha, data in enumerate(datas):
                data_atualizada = pd.to_datetime(data, dayfirst=True)
                data_mes_div = formatar_data(data_atualizada)
                valor_ind_div = buscar_indice(data_mes_div, indice)
                valor_ind_mes_atual = obter_indice_mes_atual(indice)

                valor_div_corre = valor_corr_infl(int(lista_valores[num_linha]), valor_ind_div, valor_ind_mes_atual)  
                lista_valores_att_infl.append(valor_div_corre)

                multa_mes_2p = multa_2_porcento(valor_div_corre)
                lista_valores_multa_2p.append(multa_mes_2p)

                multa_mes_1p_dia = multa_1_porcento_mes(data_atualizada, valor_div_corre)
                lista_valores_multa_1p.append(multa_mes_1p_dia)

                lista_valor_soma_mes.append(valor_div_corre + multa_mes_2p + multa_mes_1p_dia)                

            sub_total_divida = round(sum(lista_valor_soma_mes), 2)
            valor_somado_divida = round(multa_20_porcento(sub_total_divida), 2)

            # Mostrar DataFrame no topo
            st.write("**Detalhes do Processo:**")
            st.write(f'Aluno : {aluno}')
            df_resultado = pd.DataFrame({
                'Data parcela': datas,
                'Valor nominal': lista_valores,
                'Valor atualizado (INPC)': lista_valores_att_infl,
                'Multa 1%': lista_valores_multa_1p,
                'Multa 2%': lista_valores_multa_2p
            })
            st.dataframe(df_resultado)

            st.write(f'Subtotal da dívida: R${sub_total_divida}')
            st.write(f'Valor total com honorários: R${valor_somado_divida}')

            if st.button('Ver Propostas'):
                st.session_state.resultado_df = df_resultado
                st.session_state.sub_total_divida = sub_total_divida
                st.session_state.valor_somado_divida = valor_somado_divida
                st.session_state.propostas = calcular_propostas(sub_total_divida)
                st.sidebar.radio('Escolha uma página:', ['Consulta de Processos', 'Propostas'], index=1)

        else:
            st.error('Por favor, insira um número de processo válido.')

elif page == 'Propostas':
    st.title('Propostas de Pagamento')

    if 'resultado_df' in st.session_state:
        st.write("**Detalhes do Processo:**")
        st.dataframe(st.session_state.resultado_df)

        st.write(f'Subtotal da dívida: R${st.session_state.sub_total_divida}')
        st.write(f'Valor total com honorários: R${st.session_state.valor_somado_divida}')

        st.write("**Propostas de Pagamento:**")
        for descricao, valor in st.session_state.propostas.items():
            st.write(f'{descricao}: R${valor}')

    else:
        st.error('Por favor, realize uma consulta de processo primeiro.')
