import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc

dash.register_page(
    __name__, path='/presentacion-propuestas-y-cotizaciones-de-estudios')

data = pd.read_excel(open(
    'pages/presentacion_de_propuestas_y_cotizaciones_de_estudios.xlsx', 'rb'), sheet_name='1')

data_2 = pd.read_excel(open(
    'pages/presentacion_de_propuestas_y_cotizaciones_de_estudios.xlsx', 'rb'), sheet_name='2')

data_3 = pd.read_excel(open(
    'pages/presentacion_de_propuestas_y_cotizaciones_de_estudios.xlsx', 'rb'), sheet_name='3')

data_4 = pd.read_excel(open(
    'pages/presentacion_de_propuestas_y_cotizaciones_de_estudios.xlsx', 'rb'), sheet_name='4')

data_5 = pd.read_excel(open(
    'pages/presentacion_de_propuestas_y_cotizaciones_de_estudios.xlsx', 'rb'), sheet_name='5')

# logros alcanzados
data = data.drop(columns=['area', 'programa', 'actividad', 'actividadDetalle'])

new_cols = ['facultad', 'anio', 'Logro']
data = data[new_cols]

# Propuestas realizadas en la modalidad de servicios académicos
data_2 = data_2.drop(
    columns=['area', 'programa', 'actividad', 'actividadDetalle'])

new_cols_2 = ['facultad', 'anio', 'cifra']
data_2 = data_2[new_cols_2]
data_2["anio"] = data_2["anio"].astype('str')
data_2.fillna(0, inplace=True)
data_2['cifra'] = data_2['cifra'].astype('int')


def total_function(facultad, anio):
    df_facultad = data_2[data_2['facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    data_2.loc[(data_2['facultad'] == facultad) & (
        data_2['anio'] == anio), 'total'] = df_total


data_2.apply(lambda x: total_function(x['facultad'], x['anio']), axis=1)
total_data_2 = data_2['cifra'].sum()

# Propuestas en la modalidad de servicios académicos aprobadas por el Consejo de facultad
data_3 = data_3.drop(
    columns=['area', 'programa', 'actividad', 'actividadDetalle'])

new_cols_3 = ['facultad', 'anio', 'cifra']
data_3 = data_3[new_cols_3]
data_3["anio"] = data_3["anio"].astype('str')
data_3.fillna(0, inplace=True)
data_3['cifra'] = data_3['cifra'].astype('int')


def total_function_3(facultad, anio):
    df_facultad = data_3[data_3['facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    data_3.loc[(data_3['facultad'] == facultad) & (
        data_3['anio'] == anio), 'total'] = df_total


data_3.apply(lambda x: total_function_3(x['facultad'], x['anio']), axis=1)
total_data_3 = data_3['cifra'].sum()

# Propuestas realizadas en la modalidad de educación continua
data_4 = data_4.drop(
    columns=['area', 'programa', 'actividad', 'actividadDetalle'])

new_cols_4 = ['facultad', 'anio', 'cifra']
data_4 = data_4[new_cols_4]
data_4["anio"] = data_4["anio"].astype('str')
data_4.fillna(0, inplace=True)
data_4['cifra'] = data_4['cifra'].astype('int')


def total_function_4(facultad, anio):
    df_facultad = data_4[data_4['facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    data_4.loc[(data_4['facultad'] == facultad) & (
        data_4['anio'] == anio), 'total'] = df_total


data_4.apply(lambda x: total_function_4(x['facultad'], x['anio']), axis=1)
total_data_4 = data_4['cifra'].sum()

# Propuestas en la modalidad de educación continua aprobadas por el Consejo de facultad
data_5 = data_5.drop(
    columns=['area', 'programa', 'actividad', 'actividadDetalle'])

new_cols_5 = ['facultad', 'anio', 'cifra']
data_5 = data_5[new_cols_5]
data_5["anio"] = data_5["anio"].astype('str')
data_5.fillna(0, inplace=True)
data_5['cifra'] = data_5['cifra'].astype('int')


def total_function_5(facultad, anio):
    df_facultad = data_5[data_5['facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    data_5.loc[(data_5['facultad'] == facultad) & (
        data_5['anio'] == anio), 'total'] = df_total


data_5.apply(lambda x: total_function_5(x['facultad'], x['anio']), axis=1)
total_data_5 = data_5['cifra'].sum()

layout = html.Div([
    html.H2('Extensión, Innovación y Propiedad Intelectual'),
    html.H3('Proyectos de extensión'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Presentación de propuestas y cotizaciones de estudios",
                                    active=True, href="/presentacion-propuestas-y-cotizaciones-de-estudios")),
            dbc.NavItem(dbc.NavLink('Participación en procesos de contratación y convocatorias',
                                    href="/participacion-en-procesos-de-contratacion-y-convocatorias")),
            dbc.NavItem(dbc.NavLink('Participación en procesos de invitación directa',
                                    href="/participacion-en-procesos-de-invitacion-directa")),
            dbc.NavItem(dbc.NavLink('Proyectos iniciados en el año',
                                    href="/proyectos-iniciados-en-el-anio")),
            dbc.NavItem(dbc.NavLink('Logros en los proyectos',
                                    href="/logros-en-los-proyectos")),
            dbc.NavItem(dbc.NavLink('Liquidación de proyectos',
                                    href="/liquidacion-de-proyectos")),
        ],
        pills=True,),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Propuestas realizadas en la modalidad de servicios académicos",
                                            className="card-subtitle"),

                                    html.P(
                                        total_data_2,
                                        className="card-text",
                                        style={'textAlign': 'center'}
                                    ),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Propuestas en la modalidad de servicios académicos aprobadas por el Consejo de facultad",
                                            className="card-subtitle"),

                                    html.P(
                                        total_data_3,
                                        className="card-text",
                                        style={'textAlign': 'center'}
                                    ),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Propuestas realizadas en la modalidad de educación continua",
                                            className="card-subtitle"),

                                    html.P(
                                        total_data_4,
                                        className="card-text",
                                        style={'textAlign': 'center'}
                                    ),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Propuestas en la modalidad de educación continua aprobadas por el Consejo de facultad",
                                            className="card-subtitle"),

                                    html.P(
                                        total_data_5,
                                        className="card-text",
                                        style={'textAlign': 'center'}
                                    ),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.H5('Propuestas realizadas en la modalidad de servicios académicos'),
    dcc.Graph(id="graph_propuestas_servicios_academicos",
              figure=px.bar(data_2,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'propuetas de servicios académicos'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "anio": True},
                            barmode="group"
                            )),
    html.H5('Propuestas en la modalidad de servicios académicos aprobadas por el Consejo de facultad'),
    dcc.Graph(id="graph_propuestas_consejo_facultad",
              figure=px.bar(data_3,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'propuestas de servicios académicos aprobadas'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "anio": True},
                            )),
    html.H5('Propuestas realizadas en la modalidad de educación continua'),
    dcc.Graph(id="graph_propuestas_educacion_continua",
              figure=px.bar(data_4,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'propuestas de educación contínua'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "anio": True},
                            )),
    html.H5('Propuestas en la modalidad de educación continua aprobadas por el Consejo de facultad'),
    dcc.Graph(id="graph_propuestas_educacion_continua_consejo_facultad",
              figure=px.bar(data_5,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'propuestas de educación contínua aprobadas'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "anio": True},
                            )),
    html.H5('Logros Alcanzados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_propuestas_y_cotizacion_de_estudios",
                            options=data['facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_propuestas_y_cotizacion_de_estudios",
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
                                id='logros_table_propuestas_y_cotizacion_de_estudios',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),

], className='layout')


@callback(
    Output("logros_table_propuestas_y_cotizacion_de_estudios", "data"),
    [Input("facultad_propuestas_y_cotizacion_de_estudios", "value"), Input("anio_propuestas_y_cotizacion_de_estudios", "value")])
def logros_alcanzados_propuestas_y_cotizacion_de_estudios(facultad, anio):
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
