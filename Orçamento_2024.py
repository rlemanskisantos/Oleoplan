import streamlit as st
from pathlib import Path
import pandas as pd
from datetime import datetime, date
import calendar
import plotly.express as px

### Configura o layout para ser mais amplo, insere título e logo
st.set_page_config(page_title="Gestão Orçamentária",
                   page_icon=":chart_with_upwards_trend:",
                   layout="wide")
st.title("Orçamento 2024")
logo_path = "Logo Oleoplan JPEG.jpg"
st.image(logo_path, width=100)



    ####################################################


@st.cache_data
def load_data():

    Path(__file__)
    ### Caminho da pasta raiz
    pasta_raiz = Path(__file__).parent.parent


    ### Planilha Orçado

    pasta_orcado = pasta_raiz / 'Python - Documentos/Orçamento'
    #pasta_orcado = pasta_raiz / 'Python - Documentos/Orçamento'

    df_orcado = pd.read_excel(pasta_orcado / 'Base_Orcamento2024_v4.xlsx', sheet_name='Orcamento_Consolidado')
    orcado = df_orcado.rename(columns={'Sigla_Empresa':'Empresa',
                                    'Nome_Filial': 'Filial',
                                    'Nome_CCu': 'Centro de Custo',
                                    'Nome_NG': 'Natureza de Gastos',
                                    'Responsavel_CCu':'Responsável CCu',
                                    'Nome_TipoBase':'Tipo de Base',
                                    'Total':'Valor Orcado'})
    orcado = orcado[['Data','Empresa','Filial','Centro de Custo','Natureza de Gastos', 'Responsável CCu','Valor Orcado', 'Pacote', 'Responsável Pacote']]
    orcado['Fornecedor'] = None
    orcado['Observação'] = None

    orcado['Data'] = pd.to_datetime(orcado['Data'])


    ### Planilha Realizado Mensal fechado

    pasta_realizado = pasta_raiz / 'Python - Documentos/Orçamento'
    df_realizado_fechado = pd.read_excel(pasta_realizado / 'Base_Acompanhamento_Mensal1.xlsx', sheet_name='2 - Base de Acompanhamento')
    df_realizado_fechado = df_realizado_fechado[['Data','Empresa','Filial','Centro de Custo','Natureza de Gastos', 'Responsável CCu','Tipo de Base','Valor Realizado', 'Fornecedor', 'Observação', 'Pacote', 'Responsável Pacote']]

    realizado_fechado = df_realizado_fechado.loc[df_realizado_fechado['Tipo de Base'] == 'Realizado']
    realizado_fechado = realizado_fechado[['Data','Empresa','Filial','Centro de Custo','Natureza de Gastos', 'Responsável CCu','Valor Realizado', 'Fornecedor', 'Observação', 'Pacote', 'Responsável Pacote']]
    realizado_fechado['Data'] = pd.to_datetime(realizado_fechado['Data'])
    ultimo_mes_fechado = realizado_fechado['Data'].max().month


    ### Planilha Realizado Previas Intrames

    pasta_realizado = pasta_raiz / 'Python - Documentos/Orçamento'
    df_realizado_previa = pd.read_excel(pasta_realizado / 'Base_Acompanhamento_Decendial.xlsx', sheet_name='2 - Base de Acompanhamento')
    df_realizado_previa = df_realizado_previa[['Data','Empresa','Filial','Centro de Custo','Natureza de Gastos', 'Responsável CCu','Tipo de Base','Valor Realizado', 'Fornecedor', 'Observação', 'Pacote', 'Responsável Pacote']]

    realizado_previa = df_realizado_previa.loc[df_realizado_previa['Tipo de Base'] == 'Realizado']
    realizado_previa = realizado_previa[['Data','Empresa','Filial','Centro de Custo','Natureza de Gastos', 'Responsável CCu','Valor Realizado', 'Fornecedor', 'Observação', 'Pacote', 'Responsável Pacote']]

    realizado_previa['Data'] = pd.to_datetime(realizado_previa['Data'])

    realizado_previa = realizado_previa.loc[realizado_previa['Data'].dt.month > ultimo_mes_fechado]


    ### Mesclar tabelas

    tabela_orcamento = pd.concat([orcado, realizado_fechado, realizado_previa])

    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('IRAQUARA', 'Iraquara'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('VERANÓPOLIS', 'Veranópolis'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('CACOAL', 'Cacoal'))                                                                                  
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('TOMÉ-AÇU', 'Tomé-Açu'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('MATRIZ', 'Matriz'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('PASSO FUNDO', 'Passo Fundo'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('LAGOA VERMELHA 2', 'Lagoa Vermelha 2'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('ESTAÇÃO', 'Estação'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('MUITOS CAPÕES', 'Muitos Capões'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('TUPANCI DO SUL', 'Tupanci do Sul'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('ESMERALDA', 'Esmeralda'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('IPÊ', 'Ipê'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('CAPÃO BONITO DO SUL 12', 'Capão Bonito do Sul 12'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('CAPÃO BONITO DO SUL 13', 'Capão Bonito do Sul 13'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('TURVO', 'Turvo'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('PONTÃO', 'Pontão'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('MATO CASTELHANO', 'Mato Castelhano'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('SANTO EXPEDITO DO SUL', 'Santo Expedito do Sul'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('CAPÃO DO CEDRO', 'Capão do Cedro'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('CHARRUA', 'Charrua'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('LUÍS EDUARDO MAGALHÃES', 'Luís Eduardo Magalhães'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('JACUTINGA', 'Jacutinga'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('VILA MARIA', 'Vila Maria'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('SERTÃO', 'Sertão'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('ERECHIM', 'Erechim'))
    tabela_orcamento['Filial'] = tabela_orcamento['Filial'].apply(lambda x: x.replace('VILA FLORES', 'Vila Flores'))


    tabela_orcamento['Valor Orcado'] = tabela_orcamento['Valor Orcado'].fillna(0)
    tabela_orcamento['Valor Realizado'] = tabela_orcamento['Valor Realizado'].fillna(0)
    tabela_orcamento['Responsável Pacote'] = tabela_orcamento['Responsável Pacote'].fillna('Quem?')

    
    return tabela_orcamento

tabela_orcamento = load_data()
st.session_state['Tabela Orçamento'] = tabela_orcamento


####################################################


### Adiciona filtro para a data

data_min = tabela_orcamento['Data'].min()
data_max = tabela_orcamento['Data'].max()
hoje = datetime.now()


col1, col2 = st.columns(2)

with col1:
    opcao_data = st.radio("Selecione o período desejado: ",
                        options=["Mês Atual", "Acumulado Anual", "Mês Anterior", "Outro Período"])
    
if opcao_data == "Mês Atual":
    filtro_data = (datetime(hoje.year, hoje.month ,1,0,0),
                datetime(hoje.year, hoje.month ,hoje.day,0,0))
    
    filtro_data_inicio = filtro_data[0].strftime("%d/%m/%Y")
    filtro_data_fim = filtro_data[1].strftime("%d/%m/%Y")

    with col2:
        st.write('📆 Seleção entre {} e {}:'.format(filtro_data_inicio, filtro_data_fim))
    

elif opcao_data == "Acumulado Anual":
    filtro_data = (datetime(data_min.year, data_min.month ,1,0,0),
                datetime(hoje.year, hoje.month ,hoje.day,0,0))
    
    filtro_data_inicio = filtro_data[0].strftime("%d/%m/%Y")
    filtro_data_fim = filtro_data[1].strftime("%d/%m/%Y")

    with col2:
        st.write('📆 Seleção entre {} e {}:'.format(filtro_data_inicio, filtro_data_fim))
    

elif opcao_data == "Mês Anterior":
    num_dias_mes_ant = calendar.monthrange(hoje.year, hoje.month-1)[1]
    filtro_data = (datetime(hoje.year, hoje.month-1 ,1,0,0),
                datetime(hoje.year, hoje.month-1 , num_dias_mes_ant,0,0))
    
    filtro_data_inicio = filtro_data[0].strftime("%d/%m/%Y")
    filtro_data_fim = filtro_data[1].strftime("%d/%m/%Y")

    with col2:
        st.write('📆 Seleção entre {} e {}:'.format(filtro_data_inicio, filtro_data_fim))
    
else:
    with col2:
        filtro_data = st.date_input("Escolha o período:",
                                    min_value=datetime(data_min.year, data_min.month ,data_min.day,0,0),
                                    max_value=datetime(data_max.year, data_max.month ,data_max.day,0,0),
                                    value=(datetime(hoje.year, hoje.month ,1,0,0),
                                        datetime(hoje.year, hoje.month ,hoje.day,0,0)),
                                    format="DD/MM/YYYY")


filtro_data_lista = list(filtro_data)
data_selec_inicio = datetime.combine(filtro_data_lista[0], datetime.min.time())
data_selec_fim = datetime.combine(filtro_data_lista[1], datetime.min.time())

    
### Filtra responsáveis

responsavel_filtro = st.selectbox('Selecione o Responsável:', tabela_orcamento['Responsável CCu'].unique())

### Filtra as empresas que o responsável possui CC

dict_Resp_Emp = {}

for responsavel in tabela_orcamento['Responsável CCu'].unique():
    dict_Resp_Emp[responsavel] = tabela_orcamento.loc[tabela_orcamento['Responsável CCu'] == responsavel]['Empresa'].unique()

empresas = dict_Resp_Emp[responsavel_filtro].tolist()
empresa_filtro = st.sidebar.radio('Selecione a Empresa:', empresas).split(',')

st.sidebar.divider()

### Filtra as filiais que o responsável possui CC

dict_Resp_Fil = {}

for responsavel in tabela_orcamento['Responsável CCu'].unique():
    dict_Resp_Fil[responsavel] = tabela_orcamento.loc[(tabela_orcamento['Responsável CCu'] == responsavel)]['Filial'].unique()


### Seleciona as filiais de certa empresa para certo responsavel

if empresa_filtro[0] == 'SA':
    emp_fil = tabela_orcamento.loc[tabela_orcamento['Empresa'] == 'SA', 'Filial'].unique()
elif empresa_filtro[0] == 'NE':
    emp_fil = tabela_orcamento.loc[tabela_orcamento['Empresa'] == 'NE', 'Filial'].unique()
elif empresa_filtro[0] == 'PA':
    emp_fil = tabela_orcamento.loc[tabela_orcamento['Empresa'] == 'PA', 'Filial'].unique()
elif empresa_filtro[0] == 'RO':
    emp_fil = tabela_orcamento.loc[tabela_orcamento['Empresa'] == 'RO', 'Filial'].unique()


filiais = dict_Resp_Fil[responsavel_filtro].tolist()

filtro_comum = [item for item in emp_fil if item in filiais]

filial_filtro = st.sidebar.radio('Selecione a Filial:', filtro_comum).split(',')

### Aplica os filtros desejados

tabela_filtrada = tabela_orcamento[(tabela_orcamento['Responsável CCu'] == responsavel_filtro) &
                                (tabela_orcamento['Empresa'].isin(empresa_filtro)) &
                                (tabela_orcamento['Filial'].isin(filial_filtro)) &
                                (tabela_orcamento['Data'] >= data_selec_inicio) & (tabela_orcamento['Data'] <= data_selec_fim)]



# Função para carregar o DataFrame salvo ou criar um novo se não existir
def load_or_create_dataframe():
    try:
        # Tente carregar o DataFrame salvo
        df_comentarios = pd.read_csv("dados_registro_orcamento.csv")
    except FileNotFoundError:
        # Se o arquivo não existir, crie um DataFrame vazio
        df_comentarios = pd.DataFrame(columns=['Data',
                                            'Empresa',
                                            'Filial',
                                            'Centro de Custo',
                                            'Natureza de Gastos',
                                            'Responsável CCu',
                                            'Valor Orçado',
                                            'Valor Realizado',
                                            'Motivo',
                                            'Comentário',
                                            'Plano de Ação'])
    return df_comentarios

# Função para salvar o DataFrame em um arquivo CSV
def save_dataframe(df_comentarios):
    df_comentarios.to_csv("dados_registro_orcamento.csv", index=False)

# Carrega ou cria o DataFrame
df_comentarios = load_or_create_dataframe()



### Cria uma tabela dinâmica expandível para cada Centro de Custo

for centro_custo_filtro in tabela_filtrada['Centro de Custo'].unique():
    ### Cria um expander para cada Centro de Custo
    with st.expander(f"Centro de Custo: {centro_custo_filtro}"):
        ### Filtrar o DataFrame para o 'Centro de Custo' específico
        df_CC = tabela_filtrada[(tabela_filtrada['Centro de Custo'] == centro_custo_filtro)]
        df_filtrado = df_CC.groupby('Natureza de Gastos').agg({'Valor Realizado': 'sum',
                                                                'Valor Orcado': 'sum'})
        ### Adiciona variação entre orçado e realizado
        df_filtrado['Variacao R$'] = df_filtrado['Valor Realizado'] - df_filtrado['Valor Orcado']
        df_filtrado['Variacao %'] = (df_filtrado['Variacao R$'] / df_filtrado['Valor Orcado']).map('{:.2%}'.format)

        df_filtrado = df_filtrado.sort_values(by='Natureza de Gastos')

        tab1, tab2, tab3, tab4 = st.tabs(["📖 Dados", "📈 Gráfico", "🔍 Histórico", "⌨️ Registro"])
        
        # Define uma função para formatar números em formato brasileiro

        def formatar_numero_br(numero):
            # Verifica se o valor é numérico
            if isinstance(numero, (int, float)):
                return "{:,.0f}".format(numero).replace(',', '.')
            else:
                return numero


        with tab1:
            tab1.subheader("Tabela por Natureza de Gastos")
            colunas_selecionadas = ['Valor Orcado', 'Valor Realizado','Variacao R$','Variacao %']
            total1, total2, total3, total4, total5 = st.columns(5)
            with total1:
                total1.title("Total")
            with total2:
                total2.metric("Gasto Orçado, R$", "{:,.0f}".format(df_filtrado['Valor Orcado'].sum()).replace(',', '.'))
            with total3:
                total3.metric("Gasto Realizado, R$", "{:,.0f}".format(df_filtrado['Valor Realizado'].sum()).replace(',', '.'))
            with total4:
                total4.metric("Delta, R$", "{:,.0f}".format(df_filtrado['Variacao R$'].sum()).replace(',', '.'))  
            with total5:
                total5.metric("Delta, %", f"{df_filtrado['Variacao R$'].sum()/df_filtrado['Valor Orcado'].sum() * 100:.0f}%")  

                
            # Aplica a formatação aos dados do DataFrame
            df_filtrado_formatado = df_filtrado.applymap(formatar_numero_br)

            # Exibe o DataFrame formatado no Streamlit
            st.dataframe(df_filtrado_formatado[colunas_selecionadas], width=1000)


        with tab2:
            #tab2.subheader("Comparação de Valores Orçados vs Realizados de {}".format(responsavel_filtro))
            colors = {'Valor Orcado': 'gray', 'Valor Realizado': 'orange'}
            fig = px.bar(df_filtrado, y=['Valor Orcado', 'Valor Realizado'], barmode='group', color_discrete_map = colors)
            fig.update_xaxes(tickangle=270)
            fig.update_layout(title='Orçamento 2024',
                            xaxis_title='Naturezas de Gastos',
                            yaxis_title='Valor',
                            )
            st.plotly_chart(fig)

        with tab3:
            #tab3.header("Você tem x comentarios pendentes")

            counter = 0
            comentarios_pendentes = 0
            natureza_comentario = {}

            naturezas_ordenadas = sorted(tabela_filtrada['Natureza de Gastos'].unique())
            for natureza_filtro in naturezas_ordenadas:

                ### Filtrar o DataFrame para o 'Natureza' específica
                tab3.subheader("#️⃣ Abertura da Natureza {}".format(natureza_filtro), divider='blue')

                df_CC_nat = df_CC[df_CC['Natureza de Gastos'] == natureza_filtro]
                gasto_nat = df_CC_nat['Valor Realizado'].sum()
                orcado_nat = df_CC_nat['Valor Orcado'].sum()
                delta_nat = gasto_nat - orcado_nat
                delta_nat_perc = delta_nat / orcado_nat
                
                col1, col2, col3 = st.columns(3)

                col1.metric("Gasto Orçado, R$", "{:,.0f}".format(orcado_nat).replace(',', '.'))
                col2.metric("Gasto Realizado, R$", "{:,.0f}".format(gasto_nat).replace(',', '.'))
                col3.metric("Delta, R$ e %", "{:,.0f}".format(delta_nat).replace(',', '.'),  f"{delta_nat_perc * 100:.0f}%")
            
                colunas_selecionadas_hist = ['Valor Realizado', 'Fornecedor', 'Observação']
                df_hist = df_CC_nat[df_CC_nat['Valor Realizado'] > 0]
                st.dataframe(df_hist[colunas_selecionadas_hist], width=1000, hide_index=True)
                

                if opcao_data == "Mês Anterior":
                    

                    if abs(delta_nat) < 100:
                        st.caption(':blue[_Não há necessidade de comentário._]')
                        
                    elif df_comentarios[(df_comentarios['Natureza de Gastos'] == natureza_filtro) &
                                        (df_comentarios['Centro de Custo'] == centro_custo_filtro) &
                                        (df_comentarios['Data'] == filtro_data[0].strftime("%m/%Y"))].empty:
                        
                        if abs(delta_nat_perc) > 0.1 or abs(delta_nat) > 100000:
                            st.caption(':red[⚠️ _Favor comentar sobre a variação._]')
                            natureza_comentario[natureza_filtro] = True
                            comentarios_pendentes = comentarios_pendentes + 1
                        else:
                            st.caption(':blue[_Não há necessidade de comentário._]')

                    else:
                        st.caption(':green[✅ _Comentário já realizado._]')
                                            
                    counter = counter + 1

                    col1, col2, col3 = st.columns(3)
                    
                    comentario_key = f'comentario_{centro_custo_filtro}_{natureza_filtro}_{responsavel_filtro}_{counter}'
                    with col1:
                        motivo = st.selectbox('Selecione o motivo:', ('Mudança de preços',
                                                                    'Variação de produção/consumo',
                                                                    'Gasto não planejado',
                                                                    'Deslocamento temporal',
                                                                    'Outro'), key=f"{comentario_key}", index=None, placeholder="Selecione o motivo...")

                    with col2:
                        comentario = st.text_area(f'Comentário:', key=f"{comentario_key}_{counter}")
                    with col3:
                        plano_de_acao = st.text_area(f'Plano de ação:', key=f"{comentario_key}_{counter}_{counter}")


                    if st.button(f'Salvar Comentário para {natureza_filtro}', key=f'salvar_{comentario_key}'):

                        # Adicionar os dados ao DataFrame
                        novo_dado = {'Data': filtro_data[0].strftime("%m/%Y"),
                                    'Empresa': empresa_filtro,
                                    'Filial': filial_filtro,
                                    'Centro de Custo': centro_custo_filtro,
                                    'Natureza de Gastos': natureza_filtro,
                                    'Responsável CCu': responsavel_filtro,
                                    'Valor Orçado': orcado_nat,
                                    'Valor Realizado': gasto_nat,
                                    'Motivo': motivo,
                                    'Comentário': comentario,
                                    'Plano de Ação': plano_de_acao}
                        
                        df_comentarios = pd.concat([df_comentarios, pd.DataFrame(novo_dado)], ignore_index=True)
                        
                        # Salva o DataFrame atualizado

                        save_dataframe(df_comentarios)
                        st.success("Dados salvos com sucesso!")
            
        with tab4:
            # if st.session_state["username"] == "admin":
            #     # Inicializa um dicionário para armazenar as naturezas de gastos sem comentários

            #     naturezas_sem_comentarios = {}

            #     # Determina os meses anteriores ao "mês anterior" com base no filtro de data selecionado
            #     mes_anterior = datetime(hoje.year, hoje.month - 1, 1, 0, 0)
            #     meses_anteriores = pd.date_range(end=mes_anterior, start=data_min).strftime('%m/%Y').tolist()

            #     # Itera sobre todos os meses anteriores e o "mês anterior"
            #     for mes in meses_anteriores:
            #         # Itera sobre todas as naturezas de gastos
            #         for natureza_filtro in naturezas_ordenadas:
            #             # Filtra o DataFrame para a natureza de gastos específica e o mês atual
            #             df_CC_nat_mes = df_CC[
            #                 (df_CC['Natureza de Gastos'] == natureza_filtro) &
            #                 (df_CC['Data'].dt.strftime('%m/%Y') == mes)
            #             ]
                        
            #             # Verifica se há um registro de comentário para esta natureza de gastos, centro de custo e mês
            #             if df_comentarios[
            #                     (df_comentarios['Natureza de Gastos'] == natureza_filtro) &
            #                     (df_comentarios['Centro de Custo'] == centro_custo_filtro) &
            #                     (df_comentarios['Data'] == mes)
            #                 ].empty:
            #                 # Se não houver registro de comentário, adiciona a natureza de gastos ao dicionário
            #                 if mes not in naturezas_sem_comentarios:
            #                     naturezas_sem_comentarios[mes] = {}
            #                 naturezas_sem_comentarios[mes][natureza_filtro] = True

            #     # Exibe as naturezas de gastos sem comentários para o administrador
            #     if naturezas_sem_comentarios:
            #         st.write("### Naturezas de gastos sem comentários nos meses anteriores e no mês anterior:")
            #         for mes, naturezas in naturezas_sem_comentarios.items():
            #             st.write(f"- Mês: {mes}")
            #             st.write("  Naturezas de gastos:")
            #             for natureza in naturezas.keys():
            #                 st.write(f"  - {natureza}")
            #     else:
            #         st.write("### Todos os responsáveis comentaram sobre todas as naturezas de gastos nos meses anteriores e no mês anterior.")
                
            #     st.divider()

            # else:
            #     pass
            
            
            #st.write("### Dados Registrados para {}".format(responsavel_filtro))
            if comentarios_pendentes > 0:
                st.write("### ⚠️Você tem {} comentários pendentes".format(comentarios_pendentes))
                st.write("Naturezas que requerem comentários:")
    
                # Itera sobre as chaves do dicionário natureza_comentario
                for natureza in natureza_comentario.keys():
                    st.write("- {}".format(natureza))

                st.write("")
            else: 
                st.write("### Não há comentários pendentes")

            st.write("")
            st.write("Registro de comentários realizados:")

            st.dataframe(df_comentarios.loc[df_comentarios['Responsável CCu'] == responsavel_filtro], hide_index=True)


############################


#SUGESTOES
    #5to flag
        # periodo para justificativa
        # só pegar o do mensal
        # e justificar pelo acumulado
    

  ####### MELHORIAS

    # analitics
    # acesso fora do ip

#SUGESTOES JOSI
    # formatar numeros OK
    # inserir total no historico da tabela OK
    # dizer que sao x comentarios pendentes para este mes e de que sao para xyz natureza filtro inserindo em cada for num dictionary OK
        #se ja comentou, tirar do dict OK
    # se ja comentou, falar no historico que ja comentou OK
    # se o cara nao comentou em um mes, como saberemos que o total nao comentado = acompanhamento OK


