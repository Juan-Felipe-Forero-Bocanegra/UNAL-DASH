import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
from flask import session
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/movilidad-estudiantil')
#server = app.server

data = pd.read_excel('pages/movilidad_estudiantil_2.xlsx')
data_2 = pd.read_excel('pages/logros.xlsx')

data["anio"] = data["anio"].astype('str')

#movilidad nacional entrante
movilidad_nacional = data[data['Nivel'] == 'Nacional']
#movilidad nacional entrante
movilidad_nacional_entrante = movilidad_nacional[movilidad_nacional['Tipo'] == 'Movilidad entrante']
movilidad_nacional_entrante = movilidad_nacional_entrante.sort_values('facultad', ascending=False)
#movilidad nacional saliente
movilidad_nacional_saliente = movilidad_nacional[movilidad_nacional['Tipo'] == 'Movilidad saliente']
movilidad_nacional_saliente = movilidad_nacional_saliente.sort_values('facultad', ascending=False)
#movilidad internacional
movilidad_internacional = data[data['Nivel'] == 'Internacional']
#movilidad internacional entrante
movilidad_internacional_entrante = movilidad_internacional[movilidad_internacional['Tipo'] == 'Movilidad entrante']
movilidad_internacional_entrante = movilidad_internacional_entrante.sort_values('facultad', ascending=False)
#movilidad internacional saliente
movilidad_internacional_saliente = movilidad_internacional[movilidad_internacional['Tipo'] == 'Movilidad saliente'] 
movilidad_internacional_saliente = movilidad_internacional_saliente.sort_values('facultad', ascending=False)

layout = html.Div([
    html.Br(),    
    html.H2('Relaciones Interinstitucionales'),
    html.Br(),  
    html.H3('Movilidad académica'),
    html.Br(),
    dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Movilidad estudiantil", active=True, href="/movilidad-estudiantil")),
        dbc.NavItem(dbc.NavLink('Movilidad docente', href="/movilidad-docente")),
    ],
    pills=True),
    html.Br(), 
    html.H5('Estudiantes beneficiados'),
    html.Br(),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        html.H5('Movilidad nacional entrante', style={'textAlign': 'center'}),
                        dcc.Graph(id="graph_movilidad_entrante_entrante",
                                    figure = px.bar(movilidad_nacional_entrante, 
                                    x="Estudiantes beneficiados", 
                                    y="facultad", 
                                    color="anio",
                                    labels={
                                        'facultad': 'Dependencia',                   
                                        'anio': 'año',
                                    },               
                                    color_discrete_sequence=px.colors.qualitative.Plotly, 
                                    hover_data={
                                            "Estudiantes beneficiados":True,                                             
                                            "anio":True}, 
                                    )),
                ]), lg=6),
                    dbc.Col(html.Div([
                        html.H5('Movilidad nacional saliente', style={'textAlign': 'center'}),
                        dcc.Graph(id="graph_movilidad_entrante_saliente",
                                    figure = px.bar(movilidad_nacional_saliente, 
                                    x="Estudiantes beneficiados", 
                                    y="facultad", 
                                    color="anio",
                                    labels={
                                        'facultad': 'Dependencia',                   
                                        'anio': 'año',
                                    },               
                                    color_discrete_sequence=px.colors.qualitative.Plotly, 
                                    hover_data={
                                            "Estudiantes beneficiados":True,                                             
                                            "anio":True}, 
                                    )),
                ]), lg=6),                   
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        html.H5('Movilidad internacional entrante', style={'textAlign': 'center'}),
                        dcc.Graph(id="graph_movilidad_internacional_entrante",
                                    figure = px.bar(movilidad_internacional_entrante, 
                                    x="Estudiantes beneficiados", 
                                    y="facultad", 
                                    color="anio",
                                    labels={
                                        'facultad': 'Dependencia',                   
                                        'anio': 'año',
                                    },               
                                    color_discrete_sequence=px.colors.qualitative.D3, 
                                    hover_data={
                                            "Estudiantes beneficiados":True,                                             
                                            "anio":True}, 
                                    )),
                ]), lg=6),
                    dbc.Col(html.Div([
                        html.H5('Movilidad internacional saliente', style={'textAlign': 'center'}),
                        dcc.Graph(id="graph_movilidad_internacional_saliente",
                                    figure = px.bar(movilidad_internacional_saliente, 
                                    x="Estudiantes beneficiados", 
                                    y="facultad", 
                                    color="anio",
                                    labels={
                                        'facultad': 'Dependencia',                   
                                        'anio': 'año',                                    },               
                                    color_discrete_sequence=px.colors.qualitative.D3, 
                                    hover_data={
                                            "Estudiantes beneficiados":True,                                             
                                            "anio":True}, 
                                    )),
                ]), lg=6),                   
                ]
            ),
        ]
    ),
    html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div([
                     dcc.Dropdown(
                        id="nivel_movilidad_estudiantil",
                        options= data['Nivel'].unique(),
                        clearable=True,
                        placeholder="Seleccione el nivel",
                    ),
                ]),lg=6),
                dbc.Col(html.Div([
                    dcc.Dropdown(
                    id="tipo_movilidad_estudiantil",
                    options= data['Tipo'].unique(),
                    clearable=True,
                    placeholder="Seleccione el tipo",
                ),

                ]),lg=6),
            ]
        ),
    ]),   
    dcc.Graph(id="graph_movilidad_estudiantil"),
    html.H5('Logros Alcanzados'),
    html.Br(),
    html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div([
                      dcc.Dropdown(
                        id="facultad_movilidad_estudiantil",
                        options= data_2['facultad'].unique(),
                        clearable=True,
                        placeholder="Seleccione la facultad",
                    ),
                ]),lg=6),
                dbc.Col(html.Div([
                    dcc.Dropdown(
                        id="anio_movilidad_estudiantil",
                        options= data_2['anio'].unique(),
                        clearable=True,
                        placeholder="Seleccione el año",
                    ),
                ]),lg=6),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        dash_table.DataTable(
                            style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(220, 220, 220)',
                                }
                            ],
                            id = 'logros_table_movilidad_estudiantil'
                        ),
                    ], style={'paddingTop': '2%'})
                )
            ]
        )
    ]),   
    html.Br(), 

], className='layout')

@callback(
    Output("graph_movilidad_estudiantil", "figure"), 
    [Input("nivel_movilidad_estudiantil", "value"), Input("tipo_movilidad_estudiantil", "value")])
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
    Output("logros_table_movilidad_estudiantil", "data"), 
    [Input("facultad_movilidad_estudiantil", "value"), Input("anio_movilidad_estudiantil", "value")])
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
