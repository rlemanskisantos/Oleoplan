import streamlit as st
from pathlib import Path
import pandas as pd
from datetime import datetime, date
import datetime
import calendar
import plotly.express as px

Path(__file__)
### Caminho da pasta raiz
pasta_raiz = Path(__file__).parent.parent


### Planilha Orçado

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
realizado_fechado['Data'].unique()

ultimo_mes_fechado = realizado_fechado['Data'].max().month
print(ultimo_mes_fechado)

realizado_fechado.style

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

hoje = datetime.datetime.now()
num_dias_mes_ant = calendar.monthrange(hoje.year, hoje.month-1)[1]

st.write('Hi')
