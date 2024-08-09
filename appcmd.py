import pandas as pd
import os

caminho = os.getcwd()

arquivo = pd.read_excel('nova.xlsx')
indice = pd.read_excel('indice.xlsx')

def dias_em_atraso(vencimento):
    """verificar a quantidade de dias em atraso em relação a data de vencimento ao dia atual

    Args:
        vencimento (float): a data em datetime

    Returns:
        float: numero de dias em atraso
    """
    
    dia_hoje = pd.to_datetime('today')
    dias_atraso = (dia_hoje - vencimento).days
    if dias_atraso < 0:
        dias_atraso = 0
    return dias_atraso

def multa_1_porcento_mes(data_inicio,valor):
    """calculo da porcentagem de 1% ao mes no calculo e usado 1/30 como padrão para validar na quantidade de dias que estão em atraso

    Args:
        dias (float): dias em atraso da fatura

    Returns:
        float: valor da multa de todos os dias em atraso usando o calculo de 1/30 x a quantidade de dias em atraso
    """
    hoje_formatado = pd.to_datetime('today')
    dias_atraso = (hoje_formatado-data_inicio).days
    porcentagem = 1/30
    porcentagem_dias = dias_atraso * porcentagem
    valor_multa = (valor * porcentagem_dias)/100
    return valor_multa    

def multa_20_porcento(valor):
    """calculo do honorários advocatícios que sao em um valor de 20 porcento em cima do valor final da divida do cliente 

    Args:
        valor (float): valor final do debito do cliente

    Returns:
        float: retorna o valor atualizado da divida somado com 20 porcento
    """
    
    
    return valor * 1.20

def multa_2_porcento(valor):
    """função que calcula 2 porcento em cima do "valor" e retorna somente o valor da multa 

    Args:
        valor (float): valor da divida ja com correção monetária

    Returns:
        float: valor somente da multa
    """
    
    return valor * 0.02


def formatar_data(data):
    """formata um datetime em mes-ano exp 30-01-2024 00:00:00 em 01-2024

    Args:
        data (datetime): uma data em formato datetime

    Returns:
        str: retorna uma str no formato 
    """
    
    data_atualizada = pd.to_datetime(data)
    return f'{data_atualizada.month}-{data_atualizada.year}'

def buscar_indice(data_formatada, df_indice):
    """retorna o indice de um mes pre estabelecido

    Args:
        data_formatada (str): data em formato mes-ano
        df_indice (dataframe): o nome da planilha onde sera consultado

    Returns:
        float: retorna um valor indice em float
    """
    
    ind_mes_div = df_indice[df_indice['data abreviada'] == data_formatada]
    return float(ind_mes_div['indice'].values[0])


def obter_indice_mes_atual(df_indice):
    """retorna o indice do mes atual caso nao seja possivel ira retorna o indice do mes anterior 

    Args:
        df_indice (dateframe): o nome da df onde sera consultado o indice

    Returns:
        float: retorna o valor de indice mais recente que se tem na planilha
    """
    
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


def valor_corr_infl(valor_div,indi_mes_div,indi_mes_atual):
    """atualiza o valor do indice dividindo o atual pelo anterior e multiplica no valor da divida para se obter um valor corrigido pela inflação

    Args:
        valor_div (float): valor da divida antiga
        indi_mes_div (float): valor indice do mes da divida
        indi_mes_atual (float): valor indice do mes atual ou mais recente

    Returns:
        flaot: valor atualizado da divida seguindo o conseito de atualização monetaria
    """
    
    
    indice_att = indi_mes_atual/indi_mes_div
    return valor_div*indice_att
    
    


def lista_menu(indice):
    linha = arquivo[arquivo['numero da planilha original'] == indice]
    lista_data = (linha['datas att'].values[0]).split(',')
    lista_valores = (linha['valor nominal'].values[0]).split(',')
    aluno = (linha['alunos'].values[0])
    return lista_data,lista_valores,aluno
    

def menu_principal():
    while True:
        print("========== MENU PRINCIPAL ==========")
        print("1. Consultar processo")
        print("2. Sair")
        print("====================================")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("digite o numero do processo que deseja consultar: ")
            
            while True:
                try:
                    numero_processo = int(input())
                    datas,lista_valores,aluno = lista_menu(numero_processo)
                    break
                # Coloque o código para consultar o processo aqui
                except:
                    print('numero de processo invalido por gentileza tentar novamente')
                    
            
            lista_valores_att_infl = []
            lista_valores_multa_1p = []
            lista_valores_multa_2p = []
            lista_valor_soma_mes = []
            sub_total_divida = ''
            valor_somado_divida = ''

            for num_linha, data in enumerate(datas):
                
                #data da fatura em datetime formato completo 01-01-2024 00:00:00
                data_atualizada = pd.to_datetime(data, dayfirst=True)
                
                #pega a data da lista de datas dos meses da divida
                data_mes_div = formatar_data(data_atualizada)
                
                #pega o valor do indice do mes da divida --referindo a linha completa anterior
                valor_ind_div = buscar_indice(data_mes_div,indice)
                
                #mes e dia no mesmo formato ja para pesquisa exp '05-2024'
                valor_ind_mes_atual = obter_indice_mes_atual(indice)
                
                valor_div_corre =  valor_corr_infl(int(lista_valores[num_linha]),valor_ind_div,valor_ind_mes_atual)  
                lista_valores_att_infl.append(valor_div_corre)
                
                multa_mes_2p = multa_2_porcento(valor_div_corre)
                lista_valores_multa_2p.append(multa_mes_2p)
                    
                multa_mes_1p_dia = multa_1_porcento_mes(data_atualizada,valor_div_corre)
                lista_valores_multa_1p.append(multa_mes_1p_dia)
                
                lista_valor_soma_mes.append(valor_div_corre + multa_mes_2p + multa_mes_1p_dia)                

            sub_total_divida = round(sum(lista_valor_soma_mes),2)

            valor_somado_divida = round(multa_20_porcento(sub_total_divida),2)
            print('\n')
            print("====================================")
            print(aluno)
            
            df = pd.DataFrame({
                'Data parcela |':datas,
                'valor nominal |' : lista_valores,
                'valor correção mone |' : lista_valores_att_infl,
                'valor multa 1% |' :lista_valores_multa_1p,
                'valor multa 2% |' :lista_valores_multa_2p
            })
            print(df)
            print('\n')
            print("====================================")
            print(f'o valor total da divida é: {valor_somado_divida:.02f}')
            print("====================================\n")
            print("========== MENU PROCESSO ==========")
            print("1. Proposta do processo")
            print("2. Sair")
            print("====================================")
            y = input()
            
            if y == '1':
                print ('PROPOSTA 1 \n')
                print('VALOR A VISTA COM 10% DE DESCONTO\n')
                print(f'valor total: R$ {(valor_somado_divida*0.9):.02f} \n \n')
                
                print ('PROPOSTA 2\n')
                print ('campo para propsota 2 \n \n')
                
                print ('PROPOSTA 3\n')
                print ('campo para propsota 3\n \n')
                
                print("========== MENU DO PROPOSTA ==========")
                print("1. Enviar email")
                print("2. Sair")
                print("====================================")
                x = input()
                    
        elif opcao == '2':
            print("Saindo...")
            break  # Sai do loop e termina o programa

        else:
            print("Opção inválida. Tente novamente.")
            
menu_principal()

