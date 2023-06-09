import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/participacion-en-procesos-de-contratacion-y-convocatorias')

data = pd.read_excel(open('pages/participacion_en_procesos_de_contratacion_y_convocatorias.xlsx', 'rb'),sheet_name='1') 

data_2 = pd.read_excel(open('pages/participacion_en_procesos_de_contratacion_y_convocatorias.xlsx', 'rb'),sheet_name='2')

data_3 = pd.read_excel(open('pages/participacion_en_procesos_de_contratacion_y_convocatorias.xlsx', 'rb'),sheet_name='3')

# logros alcanzados
data = data.drop(columns=['area','programa','actividad', 'actividadDetalle'])

new_cols = ['facultad','anio', 'Logro']
data=data[new_cols]

#Propuestas presentadas
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

#propuetas ganadoras
data_3 = data_3.drop(columns=['area','programa','actividad', 'actividadDetalle'])

new_cols_3 = ['facultad','anio', 'cifra']
data_3=data_3[new_cols_3]
data_3["anio"] = data_3["anio"].astype('str')
data_3.fillna(0,inplace=True)
data_3['cifra'] = data_3['cifra'].astype('int')

def total_function(facultad, anio):
  df_facultad = data_3[data_3['facultad'] == facultad]
  df_total = df_facultad['cifra'].sum()
  data_3.loc[(data_3['facultad'] == facultad) & (data_3['anio'] == anio), 'total'] = df_total

data_3.apply(lambda x: total_function(x['facultad'], x['anio']), axis=1)



layout = html.Div([
    html.Br(), 
    html.H2('Extensión, Innovación y Propiedad Intelectual'),
    html.Br(),  
    html.H3('Proyectos de extensión'), 
    html.Br(),
    dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Presentación de propuestas y cotizaciones de estudios", href="/presentacion-propuestas-y-cotizaciones-de-estudios")),
        dbc.NavItem(dbc.NavLink('Participación en procesos de contratación y convocatorias', active=True, href="/participacion-en-procesos-de-contratacion-y-convocatorias")),
    ],
    pills=True,),
    html.Br(), 
    html.H5('Propuestas presentadas'),
    dcc.Graph(id="graph_propuestas_presentadas",
                figure = px.bar(data_2, 
                x="cifra", 
                y="facultad", 
                color="anio",
                 labels={                   
                     'anio': 'año',
                     'facultad':'Dependencia',
                     'cifra':'Propuestas presentadas'
                 },               
                color_discrete_sequence=px.colors.qualitative.Plotly, 
                hover_data={
                        "cifra":True,
                        "total":True,       
                        "anio":True}, 
                )),
    html.H5('Propuestas ganadoras'),
    dcc.Graph(id="graph_propuestas_ganadoras",
                figure = px.bar(data_3, 
                x="cifra", 
                y="facultad", 
                color="anio",
                 labels={                   
                     'anio': 'año',
                     'facultad':'Dependencia',
                     'cifra':'Propuestas ganadoras'
                 },               
                color_discrete_sequence=px.colors.qualitative.D3, 
                hover_data={
                        "cifra":True,
                        "total":True,       
                        "anio":True}, 
                )),  
    html.H5('Logros Alcanzados'),
    html.Br(), 
    dcc.Dropdown(
        id="facultad_ppcc",
        options= data['facultad'].unique(),
        clearable=True,
        placeholder="Seleccione la facultad",
    ),
    dcc.Dropdown(
        id="anio_ppcc",
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
        id = 'logros_table_ppcc'
    ),


])



@callback(
    Output("logros_table_ppcc", "data"), 
    [Input("facultad_ppcc", "value"), Input("anio_ppcc", "value")])
def logros_alcanzados_ppcc(facultad, anio):
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