# -*- coding: utf-8 -*-
"""

@author: Vagner
"""

import streamlit as st
import pandas as pd
import basedosdados as bd
from datetime import timedelta, datetime
 
id_projeto = 'processo-seletivo-414621'
st.set_page_config(layout="wide")

st.markdown(
        """
        <style>
            .logoheader { 
                width: 20%;
                display: block;
                margin-left: auto;
                margin-right: auto;
                }
            .fade-in {
                animation: fadeIn ease 1s;
                width: 50%;
                margin: auto;
                }

            @keyframes fadeIn {
                0% {
                    opacity: 0;
                }
                100% {
                    opacity: 1;
                }
                }
            .stSpinner > div {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
            }
            
        </style>
        """,
        unsafe_allow_html=True
)

st.markdown(
    """
        <div class="fade-in">
            <img src="https://aquitemtrabalho.prefeitura.rio/wp-content/uploads/2023/03/logo-prefeitura.png" alt="Prefeitura do Rio de Janeiro" class="logoheader">
            <center><h1>Chamados de serviços públicos por perturbação de sossego no Rio de Janeiro</h1></center>
            <center><p></p></center>
        </div>
    """,
        unsafe_allow_html=True
)



#Consultas iniciais nas três tabelas:

@st.cache_data
def ler_dados():
    with st.spinner('Carregando dados...'):
        chamados_2 = bd.read_sql("SELECT * FROM datario.administracao_servicos_publicos.chamado_1746 WHERE data_inicio >= '2022-01-01' AND data_inicio < '2024-01-01' AND subtipo = 'Perturbação do sossego';", billing_project_id=id_projeto)
            
        bairros = bd.read_sql("SELECT * FROM datario.dados_mestres.bairro", billing_project_id=id_projeto)
        
        ocupacao_hot = bd.read_sql("SELECT * FROM datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos", billing_project_id=id_projeto)
        st.success('Dados carregados com sucesso!')
        return pd.DataFrame(chamados_2), pd.DataFrame(bairros), pd.DataFrame(ocupacao_hot)

dados = ler_dados()
chamados_2 = dados[0]
bairros = dados[1]
ocupacao_hot = dados[2]

#Barra Lateral
st.sidebar.header('Filtros')
tipofiltro = st.sidebar.selectbox('Selecione o filtro:', ['Intervalo Personalizado', 'Por evento'])

# Variando interativamente com base na opção escolhida
if tipofiltro == 'Intervalo Personalizado':
    # Elementos específicos para 'Intervalo Personalizado'
    data_inicio = st.sidebar.date_input("Selecione a data inicial (mín. 2022/01/01)", min_value=datetime(2022,1,1), max_value=datetime(2023,12,31), value=datetime(2023,4,1))
    data_final = st.sidebar.date_input("Selecione a data final (máx. 2023/12/31)", min_value=data_inicio, max_value=datetime(2023,12,31), value=data_inicio)
elif tipofiltro == 'Por evento':
    # Elementos específicos para 'Por evento'
    evento = st.sidebar.selectbox('Selecione o evento:', ['Carnaval', 'Réveillon', 'Rock in Rio (1)', 'Rock in Rio (2)'])
    if evento == 'Carnaval':
        data_inicio = datetime(2023,2,18)
        data_final = datetime(2023,2,21)
    elif evento == 'Réveillon':
        data_inicio = datetime(2022,12,30)
        data_final = datetime(2023,1,1)
    elif evento == 'Rock in Rio (1)':
        data_inicio = datetime(2022,9,2)
        data_final = datetime(2022,9,4)
    elif evento == 'Rock in Rio (2)': 
        data_inicio = datetime(2022,9,8)
        data_final = datetime(2022,9,11)
        
eventos = ocupacao_hot.loc[:,['evento','data_inicial','data_final','taxa_ocupacao']]
eventos['data_inicial'] = pd.to_datetime(eventos['data_inicial'])
eventos['data_final'] = pd.to_datetime(eventos['data_final'])


#============ Conteúdo ==============


data_inicio = pd.to_datetime(data_inicio)
data_final = pd.to_datetime(data_final) + timedelta(days=1)
num_dias = (data_final - data_inicio).days

chamados_filtrado = chamados_2[(chamados_2['data_inicio'] >= data_inicio) & (chamados_2['data_inicio'] < data_final)]

chamados_filtrado['data_inicio'] = pd.to_datetime(chamados_filtrado['data_inicio'])

# Criando um novo DataFrame com a contagem de chamados por dia
chamados_diario =  chamados_filtrado.groupby(chamados_filtrado['data_inicio'].dt.date).size().reset_index(name='num_chamados')
chamados_diario = chamados_diario.set_index('data_inicio')
chamados_diario.index = pd.to_datetime(chamados_diario.index)
chamados_diario.index = chamados_diario.index.strftime('%d/%m/%Y')

with st.expander("Tabelas consultadas"):
    st.write("Chamados",chamados_2)
    st.write("Bairros",dados[1])
    st.write("Ocupação Hoteleira", dados[2])

st.markdown("### Chamados por perturbação de sossego por dia")
st.write("Número de chamados no período:",int(chamados_diario[['num_chamados']].sum()))
st.write("Média diária:",int(chamados_diario[['num_chamados']].sum())/num_dias)
st.write('Contagem de Chamados por dia:', chamados_diario)
st.bar_chart(chamados_diario['num_chamados'])

st.markdown("---")

st.markdown("### Chamados por perturbação de sossego por hora")

chamados_filtrado['data_inicio'] = pd.to_datetime(chamados_filtrado['data_inicio'])

horas_do_dia = pd.date_range(start='00:00:00', end='23:59:59', freq='H').time

contagem_por_hora = pd.DataFrame(index=horas_do_dia, columns=['num_chamados'])
contagem_por_hora.index.name = 'hora'

for hora in horas_do_dia:
    chamados_na_hora = chamados_filtrado[chamados_filtrado['data_inicio'].dt.hour == hora.hour]
    contagem_por_hora.loc[hora, 'num_chamados'] = len(chamados_na_hora)

st.write('Contagem de Chamados por Hora do dia:', contagem_por_hora)
contagem_por_hora.index = contagem_por_hora.index.map(lambda x: x.strftime('%H:%M'))
st.bar_chart(contagem_por_hora['num_chamados'])

st.markdown("---")

st.markdown("### Mapa dos chamados")
st.write("Obs.: Chamados sem localização são omitidos.")
dadosmapa = chamados_filtrado
dadosmapa = dadosmapa.loc[dadosmapa['latitude'].notnull()]
st.map(data=dadosmapa, latitude='latitude', longitude='longitude')


st.markdown("### Ocupação hoteleira em grandes eventos")
st.dataframe(eventos)

st.markdown("---")

st.markdown("### Lista de chamados no período selecionado")
st.write(chamados_filtrado)

st.markdown("---")




