import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc

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
    dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Movilidad estudiantil", href="/movilidad-estudiantil")),
        dbc.NavItem(dbc.NavLink('Movilidad docente', active=True, href="/movilidad-docente")),
    ],
    pills=True,),
    html.Br(), 
    html.H5('Docentes beneficiados'),
    html.Br(),
    dcc.Dropdown(
        id="nivel_movilidad_docente",
        options= data_md['Nivel'].unique(),
        clearable=True,
        placeholder="Seleccione el nivel",
    ),
    dcc.Dropdown(
        id="tipo_movilidad_docente",
        options= data_md['Tipo'].unique(),
        clearable=True,
        placeholder="Seleccione el tipo",
    ),
    dcc.Graph(id="graph_movilidad_docente"),
    html.Br(), 
    html.H5('Logros Alcanzados'),
    html.Br(), 
    dcc.Dropdown(
        id="facultad_movilidad_docente",
        options= data_md_2['facultad'].unique(),
        clearable=True,
        placeholder="Seleccione la facultad",
    ),
    dcc.Dropdown(
        id="anio_movilidad_docente",
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
        id = 'logros_table_movilidad_docente'
    ),
 ])

@callback(
    Output("graph_movilidad_docente", "figure"), 
    [Input("nivel_movilidad_docente", "value"), Input("tipo_movilidad_docente", "value")])
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
    Output("logros_table_movilidad_docente", "data"), 
    [Input("facultad_movilidad_docente", "value"), Input("anio_movilidad_docente", "value")])
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