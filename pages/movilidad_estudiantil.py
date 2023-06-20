import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
from flask import session
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/movilidad-estudiantil')
# server = app.server

data = pd.read_excel('pages/movilidad_estudiantil_2.xlsx')
data_2 = pd.read_excel('pages/logros.xlsx')

data["anio"] = data["anio"].astype('str')

# movilidad estudiantil nacional
movilidad_estudiantil_nacional = data[data['Nivel'] == 'Nacional']

# movilidad estudiantil nacional entrante
movilidad_estudiantil_nacional_entrante = movilidad_estudiantil_nacional[movilidad_estudiantil_nacional['Tipo']
                                                 == 'Movilidad entrante']
movilidad_estudiantil_nacional_entrante = movilidad_estudiantil_nacional_entrante.sort_values(
    'facultad', ascending=False)
total_movilidad_estudiantil_nacional_entrante = movilidad_estudiantil_nacional_entrante['Estudiantes beneficiados'].sum()


# movilidad estudiantil nacional saliente
movilidad_estudiantil_nacional_saliente = movilidad_estudiantil_nacional[movilidad_estudiantil_nacional['Tipo']
                                                 == 'Movilidad saliente']
movilidad_estudiantil_nacional_saliente = movilidad_estudiantil_nacional_saliente.sort_values('facultad', ascending=False)
total_movilidad_estudiantil_nacional_saliente = movilidad_estudiantil_nacional_saliente['Estudiantes beneficiados'].sum()

# movilidad estudiantil internacional
movilidad_estudiantil_internacional = data[data['Nivel'] == 'Internacional']
# movilidad estudiantil internacional entrante
movilidad_estudiantil_internacional_entrante = movilidad_estudiantil_internacional[movilidad_estudiantil_internacional['Tipo'] == 'Movilidad entrante']
movilidad_estudiantil_internacional_entrante = movilidad_estudiantil_internacional_entrante.sort_values('facultad', ascending=False)
total_movilidad_estudiantil_internacional_entrante = movilidad_estudiantil_internacional_entrante['Estudiantes beneficiados'].sum()

# movilidad estudiantil internacional saliente
movilidad_estudiantil_internacional_saliente = movilidad_estudiantil_internacional[movilidad_estudiantil_internacional['Tipo'] == 'Movilidad saliente']
movilidad_estudiantil_internacional_saliente = movilidad_estudiantil_internacional_saliente.sort_values('facultad', ascending=False)
total_movilidad_estudiantil_internacional_saliente = movilidad_estudiantil_internacional_saliente['Estudiantes beneficiados'].sum(
)


layout = html.Div([
    html.H2('Relaciones Interinstitucionales'),
    html.H3('Movilidad académica'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Movilidad estudiantil",
                                    active=True, href="/movilidad-estudiantil")),
            dbc.NavItem(dbc.NavLink('Movilidad docente',
                                    href="/movilidad-docente")),
        ],
        pills=True),
    html.H5('Estudiantes beneficiados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Movilidad nacional entrante",
                                            className="card-subtitle"),
                            
                                    html.P(
                                        total_movilidad_estudiantil_nacional_entrante,
                                        className="card-text",
                                        style={'textAlign': 'center'}
                                    ),
                                ]
                            ),
                            style={"width": "18rem"},
                        )
                    ]), lg=3),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Movilidad nacional saliente",
                                            className="card-subtitle"),
                            
                                    html.P(
                                        total_movilidad_estudiantil_nacional_saliente,
                                        className="card-text",
                                        style={'textAlign': 'center'}
                                    ),
                                ]
                            ),
                            style={"width": "18rem"},
                        )
                    ]), lg=3),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Movilidad internacional entrante",
                                            className="card-subtitle"),
                            
                                    html.P(
                                        total_movilidad_estudiantil_internacional_entrante,
                                        className="card-text",
                                        style={'textAlign': 'center'}
                                    ),
                                ]
                            ),
                            style={"width": "18rem"},
                        )
                    ]), lg=3),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Movilidad internacional saliente",
                                            className="card-subtitle"),
                            
                                    html.P(
                                        total_movilidad_estudiantil_internacional_saliente,
                                        className="card-text",
                                        style={'textAlign': 'center'}
                                    ),
                                ]
                            ),
                            style={"width": "18rem"},
                        )
                    ]), lg=3),
                ]
            ),
        ]),
    html.H5('Movilidad nacional entrante'),
    dcc.Graph(id="graph_movilidad_estudiantil_nacional_entrante",
              figure=px.bar(movilidad_estudiantil_nacional_entrante,
                            x="Estudiantes beneficiados",
                            y="facultad",
                            color="anio",
                            labels={
                                'facultad': 'Dependencia',
                                'anio': 'año',
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "Estudiantes beneficiados": True,
                                "anio": True},
                            barmode="group"
                            )),
    html.H5('Movilidad nacional saliente'),
    dcc.Graph(id="graph_movilidad_estudiantil_nacional_saliente",
              figure=px.bar(movilidad_estudiantil_nacional_saliente,
                            x="Estudiantes beneficiados",
                            y="facultad",
                            color="anio",
                            labels={
                                'facultad': 'Dependencia',
                                'anio': 'año',
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "Estudiantes beneficiados": True,
                                "anio": True},
                            barmode="group"
                            )),
    html.H5('Movilidad internacional entrante'),
    dcc.Graph(id="graph_movilidad_estudiantil_internacional_entrante",
              figure=px.bar(movilidad_estudiantil_internacional_entrante,
                            x="Estudiantes beneficiados",
                            y="facultad",
                            color="anio",
                            labels={
                                'facultad': 'Dependencia',
                                'anio': 'año',
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "Estudiantes beneficiados": True,
                                "anio": True},
                            barmode="group"
                            )),
    html.H5('Movilidad internacional saliente'),
    dcc.Graph(id="graph_movilidad_estudiantil_internacional_saliente",
              figure=px.bar(movilidad_estudiantil_internacional_saliente,
                            x="Estudiantes beneficiados",
                            y="facultad",
                            color="anio",
                            labels={
                                'facultad': 'Dependencia',
                                'anio': 'año', },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "Estudiantes beneficiados": True,
                                "anio": True},
                            barmode="group"
                            )),
    html.H5('Logros Alcanzados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_movilidad_estudiantil",
                            options=data_2['facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_movilidad_estudiantil",
                            options=data_2['anio'].unique(),
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
                                id='logros_table_movilidad_estudiantil',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),
], className='layout')


@callback(
    Output("logros_table_movilidad_estudiantil", "data"),
    [Input("facultad_movilidad_estudiantil", "value"), Input("anio_movilidad_estudiantil", "value")])
def logros_alcanzados_movilidad_estudiantil(facultad, anio):
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
