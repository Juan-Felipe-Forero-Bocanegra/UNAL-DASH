import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
from flask import session

dash.register_page(__name__, path='/convenios')

data = pd.read_excel('pages/convenios.xlsx')

data = data.drop(columns=['area', 'programa', 'actividad', 'actividadDetalle'])
data = data.iloc[1:]

new_cols = ["facultad", "anio", "Área", "Tipo", 'Entidades', 'Logro']
data = data[new_cols]


layout = html.Div([
    html.H2('Relaciones Interinstitucionales'),
    html.H3('Convenios'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink(
                "Convenios", active=True, href="/convenios")),
            dbc.NavItem(dbc.NavLink('Fortalecimiento de redes',
                                    href="/fortalecimiento-de-redes")),
        ],
        pills=True,),
    html.H5('Descripción de los convenios'),    
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_convenios",
                            options=data['facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=4),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_convenios",
                            options=data['anio'].unique(),
                            clearable=True,
                            placeholder="Seleccione el año",
                        ),
                    ]), lg=4),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="Área_convenios",
                            options=data['Área'].unique(),
                            clearable=True,
                            placeholder="Seleccione el área",
                        ),
                    ]), lg=4),
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
                                id='convenios',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),
], className='layout')


@callback(
    Output("convenios", "data"),
    [Input("facultad_convenios", "value"), Input("anio_convenios", "value"), Input("Área_convenios", "value")])
def convenios(facultad, anio, area):
    if area or anio or facultad:
        if not anio and not facultad:
            df = data
            df = df[df['Área'] == area]
            table = df.to_dict('records')
            return table
        if not area and not facultad:
            df = data
            df = df[df['anio'] == anio]
            table = df.to_dict('records')
            return table
        if not area and not anio:
            df = data
            df = df[df['facultad'] == facultad]
            table = df.to_dict('records')
            return table
        if facultad and area and not anio:
            df = data
            df = df[df['facultad'] == facultad]
            df = df[df['Área'] == area]
            table = df.to_dict('records')
            return table
        if facultad and anio and not area:
            df = data
            df = df[df['facultad'] == facultad]
            df = df[df['anio'] == anio]
            table = df.to_dict('records')
            return table
        if area and anio and not facultad:
            df = data
            df = df[df['Área'] == area]
            df = df[df['anio'] == anio]
            table = df.to_dict('records')
            return table
        if facultad and area and anio:
            df = data
            df = df[df['facultad'] == facultad]
            df = df[df['Área'] == area]
            df = df[df['anio'] == anio]
            table = df.to_dict('records')
            return table
    df = data
    table = df.to_dict('records')
    return table


'''
@callback(
    Output("p-output", "children"),
    Input("store", "data"),
)
def update(store):
    return 'Got token ' + store.get('token')
'''
