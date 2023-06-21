import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/construccion-opinion-publica-informada')

data = pd.read_excel(open(
    'pages/construccion_opinion_publica_informada.xlsx', 'rb'), sheet_name='1')

# logros alcanzados
data = data.drop(columns=['area', 'programa', 'actividad', 'actividadDetalle'])

new_cols = ['facultad', 'anio', 'Logro']
data = data[new_cols]

layout = html.Div([
    html.H2('Extensión, Innovación y Propiedad Intelectual'),
    html.H3('Estrategia de Comunicación de la Extensión'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Estrategia de Comunicación de la Extensión", href="/estrategia-comunicacion-extension")),
            dbc.NavItem(dbc.NavLink('Construcción de una opinión pública informada', active=True, href="/construccion-opinion-publica-informada")),
        ],
        pills=True,),    
    html.H5('Logros Alcanzados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_opinion_publica_informada",
                            options=data['facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_opinion_publica_informada",
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
                                id='logros_tabla_opinion_publica_informada',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_opinion_publica_informada", "data"),
    [Input("facultad_opinion_publica_informada", "value"), Input("anio_opinion_publica_informada", "value")])
def logros_alcanzados_opinion_publica_informada(facultad, anio):
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
