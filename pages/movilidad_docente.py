import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table

dash.register_page(__name__, path='/movilidad-docente')

data_md = pd.read_excel('pages/movilidad_docente_2.xlsx')
data_md_2 = pd.read_excel('pages/logros_md.xlsx')

data_md["anio"] = data_md["anio"].astype('str')

layout = html.Div([
    html.Br(), 
    html.H2('Relaciones Interinstitucionales'), 
    html.Br(),  
    html.H3('Movilidad académica'),
    html.Br(), 
    html.H4('Movilidad docente'),
    html.Br(), 
    
    dcc.Dropdown(
        id="nivel_md",
        options= data_md['Nivel'].unique(),
        clearable=True,
        placeholder="Seleccione el nivel",
    ),
    dcc.Dropdown(
        id="tipo_md",
        options= data_md['Tipo'].unique(),
        clearable=True,
        placeholder="Seleccione el tipo",
    ),
    dcc.Graph(id="graph_md"),
    html.Br(), 
    html.H4('Logros Alcanzados'),
    html.Br(), 
    dcc.Dropdown(
        id="facultad_md",
        options= data_md_2['facultad'].unique(),
        clearable=True,
        placeholder="Seleccione la facultad",
    ),
    dcc.Dropdown(
        id="anio_md",
        options= data_md_2['anio'].unique(),
        clearable=True,
        placeholder="Seleccione el año",
    ),
    html.Br(), 
    dash_table.DataTable(
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        },
        id = 'logros_md_table'
    ),
 ])

@callback(
    Output("graph_md", "figure"), 
    [Input("nivel_md", "value"), Input("tipo_md", "value")])
def update_bar_chart_md(nivel, tipo):

    if nivel or tipo:
        if not tipo:
            df = data_md
            df = df[df['Nivel'] == nivel]
            fig = px.bar(df, 
              x="Docentes beneficiados", 
                     y="facultad", 
                    color="anio",
                    color_discrete_sequence=px.colors.qualitative.Dark2, 
                    hover_data={"Docentes beneficiados":True,
                        "total":True,        
                         "Nivel":True,
                         "Tipo":True,
                         "anio":True},  
                    barmode="group")
            return fig
        if not nivel:
            df = data_md
            df = df[df['Tipo'] == tipo]
            fig = px.bar(df, 
                    x="Docentes beneficiados", 
                    y="facultad", 
                    color="anio",
                    color_discrete_sequence=px.colors.qualitative.Dark2, 
                    hover_data={"Docentes beneficiados":True,
                        "total":True,                   
                         "Nivel":True,
                         "Tipo":True,
                         "anio":True},  
                    barmode="group")
            return fig
        if nivel and tipo:
            df = data_md
            df = df[df['Nivel'] == nivel]
            df = df[df['Tipo'] == tipo]
            fig = px.bar(df, 
                     x="Docentes beneficiados", 
                     y="facultad", 
                    color="anio",
                    color_discrete_sequence=px.colors.qualitative.Dark2, 
                    hover_data={"Docentes beneficiados":True,
                         "total": True,
                         "Nivel":True,
                         "Tipo":True,
                         "anio":True},  
                    barmode="group")
            return fig

    df = data_md
    fig = px.bar(df, x="Docentes beneficiados", y="facultad", 
                    color="anio",
                    color_discrete_sequence=px.colors.qualitative.Dark2, 
                     hover_data={"Docentes beneficiados":True,
                         "total":True,                   
                         "Nivel":True,
                         "Tipo":True,
                         "anio":True},  
                     barmode="group")
    return fig

@callback(
    Output("logros_md_table", "data"), 
    [Input("facultad_md", "value"), Input("anio_md", "value")])
def logros_alcanzados_md(facultad, anio):
    if facultad or anio:
        if not anio:
            df = data_md_2
            df = df[df['facultad'] == facultad]
            data = df.to_dict('records')
            return data
        if not facultad:
            df = data_md_2
            df = df[df['anio'] == anio]
            data = df.to_dict('records')
            return data
        if facultad and anio:
            df = data_md_2
            df = df[df['facultad'] == facultad]
            df = df[df['anio'] == anio]
            data = df.to_dict('records')
            return data
    df = data_md_2
    data = df.to_dict('records')
    return data