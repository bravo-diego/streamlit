# Analisis de Datos Categoricos para Estadisticas Oficiales: Encuesta Nacional de Calidad e Impacto Gubernamental 2017

# Centro de Investigación en Matemáticas - Maestría en Cómputo Estadístico

import squarify
import geopandas

import numpy as np
import pandas as pd
import seaborn as sns
import plotly.io as pio
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from dbfread import DBF
from sklearn.impute import KNNImputer

import streamlit as st

#alt.data_transformers.enable("vegafusion") # habilita el transformador de datos 'vegafusion' para trabajar con conjuntos de datos >5000 filas

st.set_page_config(page_title = 'ENCIG-2017', page_icon = 'Active', layout = 'wide') # streamlit configuracion
path = 'CIMAT.png'
st.image(path, width=100) # logo CIMAT

st.title("Encuesta Nacional de Calidad e Impacto Gubernamental (ENCIG) 2017") # streamlit titulo
st.subheader("Centro de Investigación en Matemáticas, A.C.") # streamlit subtitulo
st.markdown('<style>div.block-container{padding-top:1rem}</style>',unsafe_allow_html = True)
tabs = st.tabs(['Principales Resultados'])

frecuency_by_states = pd.read_csv('frecuency_by_states.csv')

st.write("# Percepción de la Ocurrencia de las Principales Problemáticas en la República Mexicana") 

col1, col2 = st.columns((2))
with  col1:
	st.markdown(
        """
        <div style='text-align: center; font-size: 36px;'>
        
        
        
            El treemap muestra cómo se distribuyen las principales problemáticas entre la población, destacando la gravedad de cada problemática en términos de su frecuencia reportada. Los dos problemas principales que afectan a la poblacion son en temas de seguridad, con una frecuencia de 27,869, y corrupción, con 21,520 casos. Estas problemáticas están representadas como las áreas más grandes en el treemap.
        </div>
        <div style='text-align: center; font-size: 36px;'>
        
        
        
            Las categorías Ninguno y Medio Ambiente son las menos frecuentes, con solo 132 y 1,054 casos, respectivamente. Estas ocupan la menor área en el treemap.
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
	fig = plt.gcf()
	ax = fig.add_subplot()
	fig.set_size_inches(16, 8)
	squarify.plot(sizes = frecuency_by_states['Frecuencia'], label = frecuency_by_states['Ploblematica'], color = sns.color_palette('PuBu_r', len(frecuency_by_states['Frecuencia'])), alpha = .7) # treemap generado utilizando la libreria squarify

	plt.axis('off')
	st.pyplot(fig)

st.write("## Nivel de Percepción de la Corrupción por Entidad Federativa") 

geographical_data_mx = geopandas.read_file("https://gist.githubusercontent.com/walkerke/76cb8cc5f949432f9555/raw/363c297ce82a4dcb9bdf003d82aa4f64bc695cf1/mx.geojson")

corruption_map = pd.read_csv('corruption_map.csv')
barplot_corruption = pd.read_csv('barplot_corruption.csv')

geographical_data_mx['state'] = geographical_data_mx['state'].replace({'Aguascalientes': 'AGS', 'Baja California': 'BC', 'Baja California Sur': 'BCS', 'Campeche': 'CAMP', 'Coahuila de Zaragoza': 'COAH', 'Colima': 'COL', 'Chiapas': 'CHIS', 'Chihuahua': 'CHIH', 'Ciudad de México': 'CDMX', 'Durango': 'DGO', 'Guanajuato': 'GTO', 'Guerrero': 'GRO', 'Hidalgo': 'HGO', 'Jalisco': 'JAL', 'México': 'MEX', 'Michoacán de Ocampo': 'MICH', 'Morelos': 'MOR', 'Nayarit': 'NAY', 'Nuevo León': 'NL', 'Oaxaca': 'OAX', 'Puebla': 'PUE', 'Querétaro': 'QRO', 'Quintana Roo': 'QR', 'San Luis Potosí': 'SLP', 'Sinaloa': 'SIN', 'Sonora': 'SON', 'Tabasco': 'TAB', 'Tamaulipas': 'TAM', 'Tlaxcala': 'TLAX', 'Veracruz de Ignacio de la Llave': 'VER', 'Yucatán': 'YUC', 'Zacatecas': 'ZAC'}) # abreviación de los nombres de las entidades federativas para garantizar compatibilidad entre los conjuntos de datos

geographical_data_mx['percent'] = corruption_map['percent']

fig, ax = plt.subplots(1, 1, figsize=(10, 6))
geographical_data_mx.plot(column = 'percent', cmap = 'OrRd', legend = True, legend_kwds = {"orientation": "horizontal"}, ax = ax)
ax.set_axis_off()

col1, col2 = st.columns((2))
with col1:
	st.pyplot(fig) # percepción de la corrupción

with col2:
	fig = px.bar(barplot_corruption, x = 'Entidad Federativa', y = 'Porcentaje')
	fig.update_layout(xaxis = {'categoryorder':'total descending'}) 
	fig.update_traces(marker_color = 'brown', marker_line_color = 'brown', marker_line_width = 1.5, opacity = 0.6)
	st.plotly_chart(fig) # nivel de percepcion de corrupcion

st.write("## Nivel de Satisfacción General con los Servicios Básicos por Entidad Federativa") 

services_satisfaction_map = pd.read_csv('services_satisfaction_map.csv')
barplot_services = pd.read_csv('barplot_services.csv')

geographical_data_mx['percent2'] = services_satisfaction_map['percent']

fig, ax = plt.subplots(1, 1, figsize=(10, 6))
geographical_data_mx.plot(column = 'percent2', cmap = 'PuBu', legend = True, legend_kwds = {"orientation": "horizontal"}, ax = ax)
ax.set_axis_off()

col1, col2 = st.columns((2))
with col1:
	st.pyplot(fig) # satisfacción general con los servicios básicos
	
with col2:
	fig = px.bar(barplot_services, x = 'Entidad Federativa', y = 'Calificacion General')
	fig.update_layout(xaxis = {'categoryorder':'total descending'}) 
	fig.update_traces(marker_color = 'steelblue', marker_line_color = 'slategray', marker_line_width = 1.5, opacity = 0.6)
	st.plotly_chart(fig) # satisfacción general con los servicios básicos

barplot_corruption_services = pd.read_csv('barplot_corruption_services.csv')

fig = go.Figure()
fig.add_trace(go.Bar(
    x = barplot_corruption_services['Entidad_Federativa'],
    y = barplot_corruption_services['Porcentaje'],
    name = 'Percepción de Corrupción',
    marker_color = 'brown', 
    #marker_line_color = 'slategray', 
    #marker_line_width = 1.5, 
    opacity = 0.8
))
fig.add_trace(go.Bar(
    x = barplot_corruption_services['Entidad_Federativa'],
    y = barplot_corruption_services['Calificacion General'],
    name = 'Nivel de Satisfacción',
    marker_color = 'steelblue',
    #marker_line_color = 'slategray',
    #marker_line_width = 1.5, 
    opacity = 0.8
))
fig.update_layout(barmode = 'group', bargroupgap = 0.10, bargap = 0.20)
fig.update_layout(
legend = dict(orientation = "h", yanchor = "bottom", y = 1.02, xanchor = "right", x = 1
))
bargroupgap = 0.1

st.plotly_chart(fig)

st.write("# Experiencias con Pagos, Trámites y Solicitudes de Servicios Públicos")

contingency_table_issues_related_services = pd.read_csv('contingency_table_issues_related_services.csv')

colors = ['lightslategray'] * 11
colors[0] = 'brown'
colors[1] = 'brown'
colors[2] = 'brown'

fig = go.Figure()
fig.add_trace(go.Bar(
    x = contingency_table_issues_related_services['index'],
    y = contingency_table_issues_related_services['% Si'],
    name = 'Frecuencia de Ocurrencia del Problema',
    marker_color = colors, 
    opacity = 0.8
))
fig.update_layout(barmode = 'group', bargroupgap = 0.10, bargap = 0.20)
bargroupgap = 0.1

st.plotly_chart(fig) 

st.write("## Problemas en el Pago, Trámite o Solicitud de Servicios de Salud")

contingency_table_health_services_updated = pd.read_csv('contingency_table_health_services_updated.csv')

colors = ['lightslategray'] * 11
colors[0] = 'brown'

fig = go.Figure()
fig.add_trace(go.Bar(
    x = contingency_table_health_services_updated['index'],
    y = contingency_table_health_services_updated['% Si'],
    name = 'Frecuencia de Ocurrencia del Problema',
    marker_color = colors,  
    opacity = 0.8
))
fig.update_layout(barmode = 'group', bargroupgap = 0.10, bargap = 0.20)
bargroupgap=0.1

st.plotly_chart(fig) # problemas en el pago, trámite o solicitud de servicios de salud

