from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table

app = Dash(__name__)
server = app.server

data = pd.read_excel('movilidad_estudiantil_2.xlsx')
data_2 = pd.read_excel('logros.xlsx')
data_md = pd.read_excel('movilidad_docente_2.xlsx')
data_md_2 = pd.read_excel('logros_md.xlsx')

data["anio"] = data["anio"].astype('str')

data_md["anio"] = data_md["anio"].astype('str')

app.layout = html.Div([    

    html.H2('Movilidad estudiantil'),
    
    dcc.Dropdown(
        id="nivel",
        options= data['Nivel'].unique(),
        clearable=True,
    ),
    dcc.Dropdown(
        id="tipo",
        options= data['Tipo'].unique(),
        clearable=True,
    ),
    dcc.Graph(id="graph"),

    html.H3('Logros Alcanzados'),

    dcc.Dropdown(
        id="facultad",
        options= data_2['facultad'].unique(),
        clearable=True,
    ),
    dcc.Dropdown(
        id="anio",
        options= data_2['anio'].unique(),
        clearable=True,
    ),
    dash_table.DataTable(
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        },
        id = 'logros_table'
    ),

    html.H2('Movilidad docente'),
    
    dcc.Dropdown(
        id="nivel_md",
        options= data_md['Nivel'].unique(),
        clearable=True,
    ),
    dcc.Dropdown(
        id="tipo_md",
        options= data_md['Tipo'].unique(),
        clearable=True,
    ),
    dcc.Graph(id="graph_md"),

    html.H3('Logros Alcanzados'),

    dcc.Dropdown(
        id="facultad_md",
        options= data_md_2['facultad'].unique(),
        clearable=True,
    ),
    dcc.Dropdown(
        id="anio_md",
        options= data_md_2['anio'].unique(),
        clearable=True,
    ),
    dash_table.DataTable(
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        },
        id = 'logros_md_table'
    ),
])


@app.callback(
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

@app.callback(
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


@app.callback(
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
    df = data_md_2
    data = df.to_dict('records')
    return data

@app.callback(
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


app.run_server()