import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/fortalecimiento-de-redes')

data = pd.read_excel('pages/fortalecimiento_redes.xlsx')

data = data.drop(columns=['area', 'programa', 'actividad', 'actividadDetalle'])
data = data.iloc[1:]

new_cols = ["facultad", "anio", 'Entidades', 'Logro']
data = data[new_cols]

layout = html.Div([
    html.H2('Relaciones Interinstitucionales'),
    html.H3('Convenios'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Convenios", href="/convenios")),
            dbc.NavItem(dbc.NavLink('Fortalecimiento de redes',
                        active=True, href="/fortalecimiento-de-redes")),
        ],
        pills=True,),
    html.H5('Logros alcanzados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_fortalecimiento_redes",
                            options=data['facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_fortalecimiento_redes",
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
                                        'backgroundColor':'rgb(29, 105, 150, 0.1)',
                                    }
                                ],
                                id='fortalecimiento_redes',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),
], className='layout')


@callback(
    Output("fortalecimiento_redes", "data"),
    [Input("facultad_fortalecimiento_redes", "value"), Input("anio_fortalecimiento_redes", "value")])
def logros_alcanzados_fortalecimiento_redes(facultad, anio):
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
