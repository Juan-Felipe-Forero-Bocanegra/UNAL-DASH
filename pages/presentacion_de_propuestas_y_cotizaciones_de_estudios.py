import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/presentacion-propuestas-y-cotizaciones-de-estudios')

data = pd.read_excel(open('pages/presentacion_de_propuestas_y_cotizaciones_de_estudios.xlsx', 'rb'),sheet_name='1') 

data_2 = pd.read_excel(open('pages/presentacion_de_propuestas_y_cotizaciones_de_estudios.xlsx', 'rb'),sheet_name='2')

data_3 = pd.read_excel(open('pages/presentacion_de_propuestas_y_cotizaciones_de_estudios.xlsx', 'rb'),sheet_name='3')

data_4 = pd.read_excel(open('pages/presentacion_de_propuestas_y_cotizaciones_de_estudios.xlsx', 'rb'),sheet_name='4')

data_5 = pd.read_excel(open('pages/presentacion_de_propuestas_y_cotizaciones_de_estudios.xlsx', 'rb'),sheet_name='5')

# logros alcanzados
data = data.drop(columns=['area','programa','actividad', 'actividadDetalle'])

new_cols = ['facultad','anio', 'Logro']
data=data[new_cols]

#Propuestas realizadas en la modalidad de servicios académicos
data_2 = data_2.drop(columns=['area','programa','actividad', 'actividadDetalle'])

new_cols_2 = ['facultad','anio', 'cifra']
data_2=data_2[new_cols_2]
data_2["anio"] = data_2["anio"].astype('str')
data_2.fillna(0,inplace=True)
data_2['cifra'] = data_2['cifra'].astype('int')

def total_function(facultad, anio):
  df_facultad = data_2[data_2['facultad'] == facultad]
  df_total = df_facultad['cifra'].sum()
  data_2.loc[(data_2['facultad'] == facultad) & (data_2['anio'] == anio), 'total'] = df_total

data_2.apply(lambda x: total_function(x['facultad'], x['anio']), axis=1)

#Propuestas en la modalidad de servicios académicos aprobadas por el Consejo de facultad
data_3 = data_3.drop(columns=['area','programa','actividad', 'actividadDetalle'])

new_cols_3 = ['facultad','anio', 'cifra']
data_3=data_3[new_cols_3]
data_3["anio"] = data_3["anio"].astype('str')
data_3.fillna(0,inplace=True)
data_3['cifra'] = data_3['cifra'].astype('int')

def total_function_3(facultad, anio):
  df_facultad = data_3[data_3['facultad'] == facultad]
  df_total = df_facultad['cifra'].sum()
  data_3.loc[(data_3['facultad'] == facultad) & (data_3['anio'] == anio), 'total'] = df_total

data_3.apply(lambda x: total_function_3(x['facultad'], x['anio']), axis=1)

#Propuestas realizadas en la modalidad de educación continua
data_4 = data_4.drop(columns=['area','programa','actividad', 'actividadDetalle'])

new_cols_4 = ['facultad','anio', 'cifra']
data_4=data_4[new_cols_4]
data_4["anio"] = data_4["anio"].astype('str')
data_4.fillna(0,inplace=True)
data_4['cifra'] = data_4['cifra'].astype('int')

def total_function_4(facultad, anio):
  df_facultad = data_4[data_4['facultad'] == facultad]
  df_total = df_facultad['cifra'].sum()
  data_4.loc[(data_4['facultad'] == facultad) & (data_4['anio'] == anio), 'total'] = df_total

data_4.apply(lambda x: total_function_4(x['facultad'], x['anio']), axis=1)

#Propuestas en la modalidad de educación continua aprobadas por el Consejo de facultad
data_5 = data_5.drop(columns=['area','programa','actividad', 'actividadDetalle'])

new_cols_5 = ['facultad','anio', 'cifra']
data_5=data_5[new_cols_5]
data_5["anio"] = data_5["anio"].astype('str')
data_5.fillna(0,inplace=True)
data_5['cifra'] = data_5['cifra'].astype('int')

def total_function_5(facultad, anio):
  df_facultad = data_5[data_5['facultad'] == facultad]
  df_total = df_facultad['cifra'].sum()
  data_5.loc[(data_5['facultad'] == facultad) & (data_5['anio'] == anio), 'total'] = df_total

data_5.apply(lambda x: total_function_5(x['facultad'], x['anio']), axis=1)


layout = html.Div([
    html.Br(), 
    html.H2('Extensión, Innovación y Propiedad Intelectual'),
    html.Br(),  
    html.H3('Proyectos de extensión'), 
    html.Br(),
    dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Presentación de propuestas y cotizaciones de estudios", active=True, href="/presentacion-propuestas-y-cotizaciones-de-estudios")),
        dbc.NavItem(dbc.NavLink('Participación en procesos de contratación y convocatorias', href="/participacion-en-procesos-de-contratacion-y-convocatorias")),
    ],
    pills=True,),
    html.Br(),   
    html.H5('Propuestas realizadas en la modalidad de servicios académicos'),
    dcc.Graph(id="graph_propuestas_servicios_academicos",
                figure = px.bar(data_2, 
                x="cifra", 
                y="facultad", 
                color="anio",
                 labels={                   
                     'anio': 'año'
                 },               
                color_discrete_sequence=px.colors.qualitative.Plotly, 
                hover_data={
                        "cifra":True,
                        "total":True,       
                        "anio":True}, 
                )),
    html.Br(),  
    html.H5('Propuestas en la modalidad de servicios académicos aprobadas por el Consejo de facultad'),
    dcc.Graph(id="graph_propuestas_consejo_facultad",
                figure = px.bar(data_3, 
                x="cifra", 
                y="facultad", 
                color="anio",
                labels={
                     'anio': 'año'
                 }, 
                color_discrete_sequence=px.colors.qualitative.D3,          
                hover_data={
                        "cifra":True,
                        "total":True,       
                        "anio":True}, 
                )),
    html.Br(),  
    html.H5('Propuestas realizadas en la modalidad de educación continua'),
    dcc.Graph(id="graph_propuestas_educacion_continua",
                figure = px.bar(data_4, 
                x="cifra", 
                y="facultad", 
                color="anio",
                labels={                     
                     'anio': 'año'
                 },  
                color_discrete_sequence=px.colors.qualitative.Alphabet,          
                hover_data={
                        "cifra":True,
                        "total":True,       
                        "anio":True}, 
                )),
    html.Br(),  
    html.H5('Propuestas en la modalidad de educación continua aprobadas por el Consejo de facultad'),
    dcc.Graph(id="graph_propuestas_educacion_continua_consejo_facultad",
                figure = px.bar(data_5, 
                x="cifra", 
                y="facultad", 
                color="anio",
                labels={                    
                     'anio': 'año'
                 },  
                color_discrete_sequence=px.colors.qualitative.Dark24,          
                hover_data={
                        "cifra":True,
                        "total":True,       
                        "anio":True}, 
                )),
    html.H5('Logros Alcanzados'),
    html.Br(), 
    dcc.Dropdown(
        id="facultad_procesos_contratacion_convocatorias",
        options= data['facultad'].unique(),
        clearable=True,
        placeholder="Seleccione la facultad",
    ),
    dcc.Dropdown(
        id="anio_procesos_contratacion_convocatorias",
        options= data['anio'].unique(),
        clearable=True,
        placeholder="Seleccione el año",
    ),
    html.Br(), 
    dash_table.DataTable(
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        },
        id = 'logros_table_procesos_contratacion_convocatorias'
    ),


])



@callback(
    Output("logros_table_procesos_contratacion_convocatorias", "data"), 
    [Input("facultad_procesos_contratacion_convocatorias", "value"), Input("anio_procesos_contratacion_convocatorias", "value")])
def logros_alcanzados(facultad, anio):
    if facultad or anio:
        if not anio:
            df = data
            df = df[df['facultad'] == facultad]
            table = df.to_dict('records')
            return table
        if not facultad:
            df = data
            df = df[df['anio'] == anio]
            table = df.to_dict('records')
            return table
        if facultad and anio:
            df = data
            df = df[df['facultad'] == facultad]
            df = df[df['anio'] == anio]
            table = df.to_dict('records')
            return table
    df = data
    table = df.to_dict('records')
    return table