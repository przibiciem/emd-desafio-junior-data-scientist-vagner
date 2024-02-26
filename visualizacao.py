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
        </style>
        """,
        unsafe_allow_html=True
)

st.markdown(
    """
        <div class="fade-in">
            <img src="https://aquitemtrabalho.prefeitura.rio/wp-content/uploads/2023/03/logo-prefeitura.png" alt="Prefeitura do Rio de Janeiro" class="logoheader">
            <center><h1>Chamados de serviços públicos na cidade do Rio de Janeiro</h1></center>
            <center><p>Para começar, vamos realizar uma consulta SQL na tabela de chamados de serviços públicos.</p></center>
        </div>
    """,
        unsafe_allow_html=True
)

@st.cache_data
def ler_dados():
    #Consultas iniciais na tabela de bairros e na tabela de ocupação em grandes eventos:
    bairros = bd.read_sql("SELECT * FROM datario.dados_mestres.bairro", billing_project_id=id_projeto)
    
    ocupacao_hot = bd.read_sql("SELECT * FROM datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos", billing_project_id=id_projeto)
    return bairros, ocupacao_hot

dados = ler_dados()
bairros = dados[0]
ocupacao_hot = dados[1]

# Filtro por data
data_inicio = st.date_input("Selecione a data inicial da consulta", min_value=datetime(2010,6,1), max_value=datetime(2024,2,22), value=datetime(2023,4,1))
# Filtro por número de dias (com limite de 31 dias)
num_dias = st.number_input("Selecione o número de dias (máx. 7)", min_value=1, max_value=7, value=1)
data_fim = data_inicio + timedelta(days=num_dias)
st.write("Data final:",data_fim - timedelta(days=1))

# Botão de consulta
botao_consulta = st.button("Consultar")
consulta = "SELECT * FROM datario.administracao_servicos_publicos.chamado_1746 WHERE data_inicio >= '" + str(data_inicio) + "' AND data_inicio < '" + str(data_fim) + "'"


# Ao clicar do botão:
if botao_consulta:
    #Realiza a consulta SQL
    chamados = bd.read_sql(consulta, billing_project_id=id_projeto)
    chamados = pd.DataFrame(chamados)
    relacaobairros = bairros.loc[:,['id_bairro','nome','subprefeitura']]
    chamadoscompleto = pd.merge(chamados, relacaobairros, on='id_bairro', how='left')
    st.markdown("---")
    st.subheader("Resultados:")
    #Número de Chamados
    nchamados = chamados.shape[0]
    chamados_por_dia = nchamados/num_dias
    nulos = int(chamados[['id_bairro']].isnull().sum())
    dados_resumo = {'Dado':['Número de chamados total', 'Média diária', 'Chamados sem localização'],'Valor': [nchamados, chamados_por_dia, nulos]}
    
    st.dataframe(dados_resumo)
    resumo = pd.DataFrame(dados_resumo)
    
    #Contagem por tipo de chamado
    contagem_por_tipo = pd.DataFrame(chamados['tipo'].value_counts())
    
    with st.expander("Agrupados por tipo de chamado"):
        st.markdown("### Agrupados por tipo de chamado")
        col1, col2 = st.columns([0.2, 0.8])
        col1.write(contagem_por_tipo)
        with col2:
            st.bar_chart(contagem_por_tipo['count'], use_container_width=True)
            
        contagem_por_bairro = chamados['id_bairro'].value_counts()
        
        # Mescla os Dataframes com base em id_bairro
        contagem_mesclado = pd.merge(contagem_por_bairro, bairros, left_index=True, right_on='id_bairro')
    
    with st.expander("Agrupados por bairro"):
        st.markdown("### Agrupados por bairro")
        contagem_por_bairro = contagem_mesclado.loc[:,['nome','count']]
        contagem_por_bairro = contagem_por_bairro.set_index('nome')
        col3, col4 = st.columns([0.2, 0.8])
        col3.write(contagem_por_bairro)
        with col4:
            st.bar_chart(contagem_por_bairro[['count']], use_container_width=True)
    
    with st.expander("Agrupados por subprefeitura"):
        st.markdown("### Agrupados por subprefeitura")
        contagem_por_subprefeitura = pd.DataFrame(chamadoscompleto['subprefeitura'].value_counts())
        col5, col6 = st.columns([0.2, 0.8])
        col5.write(contagem_por_subprefeitura)
        
        with col6:
            st.bar_chart(contagem_por_subprefeitura['count'], use_container_width=True)
        
    st.markdown("---")
    
    st.markdown("### Mapa dos chamados")
    st.write("Obs.: Chamados sem localização são omitidos.")
    dadosmapa = chamados
    dadosmapa = dadosmapa.loc[dadosmapa['latitude'].notnull()]
    st.map(data=dadosmapa, latitude='latitude', longitude='longitude')
