import streamlit as st 
import pandas as pd
import numpy as np
import gdown
import os
import plotly.express as px 
from datetime import datetime



st.title('Fallecidos por COVID-19')


# id = 1dSRlbtutz10Lgb4wiYPcWaK3w5QMUH8O
@st.experimental_memo
def download_data():
    #https://drive.google.com/uc?id=YOURFILEID\
    url = "https://drive.google.com/uc?id=1dSRlbtutz10Lgb4wiYPcWaK3w5QMUH8O"
    output = 'data.csv'
    gdown.download(url,output,quiet = False)

download_data()
#vamos a sacar el primer millon de datos:
data = pd.read_csv('data.csv', sep = ';', parse_dates= ['FECHA_CORTE', 'FECHA_FALLECIMIENTO'])
data = data[["FECHA_CORTE","FECHA_FALLECIMIENTO","EDAD_DECLARADA","SEXO", "CLASIFICACION_DEF", "DEPARTAMENTO", "PROVINCIA", "DISTRITO", "UBIGEO", "UUID"]]
#data.at[20221116,"CLASIFICACION_DEF"]="Criterio Virologico"
#data["CLASIFICACION_DEF"[data.rename({"Criterio virolÃƒÂ³gico":"Criterio virologico"})]]
#data.replace({"Criterio virolÃƒÂ³gico":"Criterio virologico"})

#st.write(data["CLASIFICACION_DEF"].unique())
data["CLASIFICACION_DEF"] = data.CLASIFICACION_DEF.map(
        {"Criterio SINADEF":"Criterio SINADEF",
        "Criterio virolÃ³gico":"Criterio virológico",
        "Criterio serolÃ³gico":"Criterio serológico",
        "Criterio investigaciÃ³n EpidemiolÃ³gica":"Criterio investigación epidemiológica",
        "Criterio clÃ­nico":"Criterio clínico",
        "Criterio radiolÃ³gico":"Criterio radiológico",
        "Criterio nexo epidemiolÃ³gico":"Criterio nexo epidemiológico"})
st.write(data)

#Crear un selector de departamento:
departamento= np.sort(data['DEPARTAMENTO'].dropna().unique())
opcion_departamento = st.selectbox('Selecciona un departamento:', departamento)
data_departamentos = data[data['DEPARTAMENTO'] == opcion_departamento]
#num_filas= len(data_departamentos.axes[0])

#Crear un selector de provincia:
provincia= np.sort(data_departamentos['PROVINCIA'].dropna().unique())
opcion_provincia = st.selectbox('Selecciona una provincia:', provincia)
data_provincia = data_departamentos[data_departamentos['PROVINCIA']==opcion_provincia]
#num_filas= len(data_provincia.axes[0])

#Crear un selector de distritos:
distrito= np.sort(data_departamentos['DISTRITO'].dropna().unique())
opcion_distrito = st.selectbox('Selecciona una distrito:', distrito)
data_distrito = data_departamentos[data_departamentos['DISTRITO']==opcion_distrito]
#num_filas= len(data_distrito.axes[0])

#st.write('Numero de registros:', num_filas)


#Crear graficas de SEXO y EDAD
data_sexo = data_distrito.SEXO.value_counts()
st.write('Distribución por SEXO: ')
st.bar_chart(data_sexo)

data_edad = data_distrito.EDAD_DECLARADA.value_counts()
st.write('Distribución por EDAD: ')
st.bar_chart(data_edad)


#departamento= np.sort(data['DEPARTAMENTO'].dropna().unique())
edad= data['EDAD_DECLARADA']

#edad= np.sort(data['EDAD_DECLARADA'].dropna().unique())
#sexo= np.sort(data['SEXO'].dropna().unique())

#Crear slider de edad:
edad_selector = st.slider('Edad del fallecido: ',
                         min_value = min(edad),
                         max_value = max(edad),
                         value = (min(edad), max(edad)))



#SELECCIÓN DE CRITERIOS
criterio = data['CLASIFICACION_DEF'].unique()
option_criterio = st.selectbox('Lista de fallecidos según el criterio ' , criterio)

departamento_selector = st.multiselect(
                                        'Departamento: ',
                                        departamento,
                                        default = departamento
)

filtro = (data['EDAD_DECLARADA'].between(*edad_selector))&(data['DEPARTAMENTO'].isin(departamento_selector))


#GRAFICO DE BARRAS DE LOS CRITERIOS
df_criterios = data[data['CLASIFICACION_DEF'] == option_criterio]
df_crit = df_criterios.CLASIFICACION_DEF.value_counts()
st.write('Distribución por criterios')
st.bar_chart(df_crit)


df_crits = data.groupby(['CLASIFICACION_DEF'], as_index = False)[['DEPARTAMENTO']+['PROVINCIA']+['DISTRITO']].count() 

#GRAFICO CIRCULAR DE LOS CRITERIOS

pie_chart = px.pie(df_crits, #tomo el dataframe
                   title = 'Lista de fallecidos según el criterio', #Titulo
                   values = 'DEPARTAMENTO',#columna
                   names = 'CLASIFICACION_DEF') #

st.plotly_chart(pie_chart) # de esta forma se va a mostrar el dataframe en Streamlit

#CUANTO FALLECIDOS HAY
st.subheader('Fallecidos por COVID-19:')
st.code(data["SEXO"].value_counts())


fecha= np.sort(data['FECHA_FALLECIMIENTO'].dropna().unique())
st.header(f"Filtros segun fechas")

#SACAMOS LA FECHA MINIMA Y MÁXIMA PARA EL SLIDER
#fecha_min = st.write(data["FECHA_FALLECIMIENTO"].min())
#fecha_max = st.write(data["FECHA_FALLECIMIENTO"].max())

opcion_fecha = st.slider(
    "Seleccione la fecha: ",
    min_value = datetime(2020,3,3),
    max_value = datetime(2022,11,19),
    value = (datetime(2020,3,3), datetime(2022,11,19)),

    format="DD/MM/YYYY")
date_var = (data["FECHA_FALLECIMIENTO"].between(*opcion_fecha))
numero_resultados = data[date_var].shape[0] ##number of availables rows
st.markdown(f'*Resultados Disponibles: {numero_resultados}*') # sale como un titulo que dice cuantos resultados tiene para ese filtro



#MAPA 


@st.experimental_memo
def download_data():
    #https://drive.google.com/uc?id=YOURFILEID/
    url = "https://drive.google.com/uc?id=10b-uWf6Io0wo3gbSSDcCjSpCIr6xwLOB"
    output = 'TB_UBIGEOS.csv'
    gdown.download(url,output,quiet = False)

download_data()

df_ubigeos = pd.read_csv('TB_UBIGEOS.csv', sep = ',')
#st.write(df_ubigeos)
#df = df_ubigeos[['longitud', 'latitud']]
#daf1=data2.rename({ 'longitud': 'lon' , 'latitud' : 'lat'})
#st.write(daf1)
#data.merge(df_ubigeos)
 #data = data.drop(columns=["FECHA_CORTE",
 # "FECHA_FALLECIMIENTO", "CLASIFICACION_DEF", "UBIGEO", "UUID"])
 
#UNIMOS AMBOS DATASETS
data['UBIGEO']= data.UBIGEO.astype(str)
df_ubigeos['ubigeo_inei']= df_ubigeos['ubigeo_inei'].astype(str)
df_ubigeos = df_ubigeos.rename(columns={"ubigeo_inei": "UBIGEO"})
#st.write(df_ubigeos)
data1= data.merge(df_ubigeos, on="UBIGEO")
st.write(data1)
#data1.rename(columns={"latitud":"lat","longitud":"lon"}, inplace=True)
#st.map(data1)

st.title("Mapa")

name_bott = ["Ver Mapa", "Ocultar Mapa"]
name = st.radio('Visualizar',name_bott,index=1)


if name == "Ver Mapa":
    data1.rename(columns={"latitud":"lat","longitud":"lon"}, inplace=True)
    st.map(data1)



