import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table

dash.register_page(__name__, path='/movilidad-estudiantil')
#server = app.server

data = pd.read_excel('pages/movilidad_estudiantil_2.xlsx')
data_2 = pd.read_excel('pages/logros.xlsx')

data["anio"] = data["anio"].astype('str')

layout = html.Div([
    html.Br(),    

    html.H2('Relaciones Interinstitucionales'),
    html.Br(),  
    html.H3('Movilidad académica'),
    html.Br(), 
    html.H4('Movilidad estudiantil'),
    html.Br(), 
    
    dcc.Dropdown(
        id="nivel",
        options= data['Nivel'].unique(),
        clearable=True,
        placeholder="Seleccione el nivel",
    ),
    dcc.Dropdown(
        id="tipo",
        options= data['Tipo'].unique(),
        clearable=True,
        placeholder="Seleccione el tipo",
    ),
    dcc.Graph(id="graph"),

    html.H4('Logros Alcanzados'),
    html.Br(), 
    dcc.Dropdown(
        id="facultad",
        options= data_2['facultad'].unique(),
        clearable=True,
        placeholder="Seleccione la facultad",
    ),
    dcc.Dropdown(
        id="anio",
        options= data_2['anio'].unique(),
        clearable=True,
        placeholder="Seleccione el año",
    ),
    html.Br(), 
    dash_table.DataTable(
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        },
        id = 'logros_table'
    ),

])

@callback(
    Output("graph", "figure"), 
    [Input("nivel", "value"), Input("tipo", "value")])
def update_bar_chart(nivel, tipo):

    if nivel or tipo:
        if not tipo:
            df = data
            df = df[df['Nivel'] == nivel]
            fig = px.bar(df, 
              x="Estudiantes beneficiados", 
                     y="facultad", 
                    color="anio",
                    color_discrete_sequence=px.colors.qualitative.Safe, 
                    hover_data={"Estudiantes beneficiados":True,
                        "total":True,        
                         "Nivel":True,
                         "Tipo":True,
                         "anio":True},  
                    barmode="group")
            return fig
        if not nivel:
            df = data
            df = df[df['Tipo'] == tipo]
            fig = px.bar(df, 
              x="Estudiantes beneficiados", 
                     y="facultad", 
                    color="anio",
                    color_discrete_sequence=px.colors.qualitative.Safe, 
                    hover_data={"Estudiantes beneficiados":True,
                        "total":True,                   
                         "Nivel":True,
                         "Tipo":True,
                         "anio":True},  
                    barmode="group")
            return fig
        if nivel and tipo:
            df = data
            df = df[df['Nivel'] == nivel]
            df = df[df['Tipo'] == tipo]
            fig = px.bar(df, 
              x="Estudiantes beneficiados", 
                     y="facultad", 
                    color="anio",
                    color_discrete_sequence=px.colors.qualitative.Safe, 
                    hover_data={"Estudiantes beneficiados":True,
                         "total": True,
                         "Nivel":True,
                         "Tipo":True,
                         "anio":True},  
                    barmode="group")
            return fig

    df = data
    fig = px.bar(df, x="Estudiantes beneficiados", y="facultad", 
                    color="anio",
                    color_discrete_sequence=px.colors.qualitative.Safe, 
                     hover_data={"Estudiantes beneficiados":True,
                         "total":True,                   
                         "Nivel":True,
                         "Tipo":True,
                         "anio":True},  
                     barmode="group")
    return fig


@callback(
    Output("logros_table", "data"), 
    [Input("facultad", "value"), Input("anio", "value")])
def logros_alcanzados(facultad, anio):
    if facultad or anio:
        if not anio:
            df = data_2
            df = df[df['facultad'] == facultad]
            data = df.to_dict('records')
            return data
        if not facultad:
            df = data_2
            df = df[df['anio'] == anio]
            data = df.to_dict('records')
            return data
        if facultad and anio:
            df = data_2
            df = df[df['facultad'] == facultad]
            df = df[df['anio'] == anio]
            data = df.to_dict('records')
            return data
    df = data_2
    data = df.to_dict('records')
    return data
