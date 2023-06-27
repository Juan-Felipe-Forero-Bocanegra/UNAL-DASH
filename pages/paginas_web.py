import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc

dash.register_page(
    __name__, path='/paginas-web')

data = pd.read_excel(open(
    'pages/paginas_web.xlsx', 'rb'), sheet_name='1')

# logros alcanzados
data = data.drop(columns=['area', 'programa', 'actividad', 'actividadDetalle'])

new_cols = ['facultad', 'anio', 'Logro']
data = data[new_cols]

layout = html.Div([
    html.H2('Gobierno y Gestión de Servicios TI'),
    html.H3(
        'Páginas web'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Repositorios de información",
                                    href="/repositorios-informacion")),
            dbc.NavItem(dbc.NavLink("Mantenimiento y actualización de servicios digitales",
                                    href="/mantenimiento-actualizacion-servicios-digitales")),
            dbc.NavItem(dbc.NavLink("Gestión de proyectos informáticos", 
                                    href="/gestion-proyectos-informaticos")),
            dbc.NavItem(dbc.NavLink("Páginas web", active=True,
                                    href="/paginas-web")),
        ],
        pills=True,),
    html.H5('Logros Alcanzados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_paginas_web",
                            options=data['facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_paginas_web",
                            options=data['anio'].unique(),
                            clearable=True,
                            placeholder="Seleccione el año",
                        ),
                    ]), lg=6),
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
                                    'fontFamily': 'Mulish',
                                    'fontSize': '18pts',
                                    'fontWeight': 400
                                },
                                style_header={
                                    'backgroundColor': 'white',
                                    'fontWeight': 'bold',
                                    'textAlign': 'center',
                                    'fontFamily': 'Mulish',
                                    'fontSize': '22pts',
                                    'fontWeight': 500
                                },
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(29, 105, 150, 0.1)',
                                    }
                                ],
                                id='logros_tabla_paginas_web',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_paginas_web", "data"),
    [Input("facultad_paginas_web", "value"), Input("anio_paginas_web", "value")])
def logros_alcanzados_paginas_web(facultad, anio):
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
