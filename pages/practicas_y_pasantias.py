import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc

dash.register_page(
    __name__, path='/practicas-y-pasantias')

data = pd.read_excel(open(
    'pages/practicas_y_pasantias.xlsx', 'rb'), sheet_name='1')

data_2 = pd.read_excel(open(
    'pages/practicas_y_pasantias.xlsx', 'rb'), sheet_name='2')

data_3 = pd.read_excel(open(
    'pages/practicas_y_pasantias.xlsx', 'rb'), sheet_name='3')

data_4 = pd.read_excel(open(
    'pages/practicas_y_pasantias.xlsx', 'rb'), sheet_name='4')

data_5 = pd.read_excel(open(
    'pages/practicas_y_pasantias.xlsx', 'rb'), sheet_name='5')

data_6 = pd.read_excel(open(
    'pages/practicas_y_pasantias.xlsx', 'rb'), sheet_name='6')

# logros alcanzados
data = data.drop(columns=['area', 'programa', 'actividad', 'actividadDetalle'])

new_cols = ['facultad', 'anio', 'Logro']
data = data[new_cols]

# Estudiantes de pregrado vínculados con entidades externas
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

# Estudiantes de posgrado vínculados con entidades externas
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

# Estudiantes de pregrado vinculados con la Universidad
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

# Estudiantes de posgrado vinculados con la Universidad
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

# Suma de los reconocmientos económicos

data_6 = data_6.drop(
    columns=['area', 'programa', 'actividad', 'actividadDetalle'])

new_cols_5 = ['facultad', 'anio', 'cifra']
data_6 = data_6[new_cols_5]
data_6["anio"] = data_6["anio"].astype('str')
data_6.fillna(0, inplace=True)
data_6['cifra'] = data_6['cifra'].astype('int')


def total_function_5(facultad, anio):
    df_facultad = data_6[data_6['facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    data_6.loc[(data_6['facultad'] == facultad) & (
        data_6['anio'] == anio), 'total'] = df_total


data_6.apply(lambda x: total_function_5(x['facultad'], x['anio']), axis=1)
total_data_6 = data_6['cifra'].sum()

layout = html.Div([
    html.H2('Extensión, Innovación y Propiedad Intelectual'),
    html.H3('Prácticas y pasantías'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Prácticas y pasantías",
                                    active=True, href="/practicas-y-pasantias")),
            dbc.NavItem(dbc.NavLink("Convenios para prácticas y pasantías",
                                     href="/convenios-practicas-pasantias-anio")),
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
                                    html.H6("Estudiantes de pregrado vínculados con entidades externas",
                                            className="card-subtitle"),

                                    html.P(
                                        total_data_2,
                                        className="card-text",
                                        style={'textAlign': 'center'}
                                    ),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=3),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Estudiantes de posgrado vínculados con entidades externas",
                                            className="card-subtitle"),

                                    html.P(
                                        total_data_3,
                                        className="card-text",
                                        style={'textAlign': 'center'}
                                    ),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=3),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Estudiantes de pregrado vinculados con la Universidad",
                                            className="card-subtitle"),

                                    html.P(
                                        total_data_4,
                                        className="card-text",
                                        style={'textAlign': 'center'}
                                    ),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=3),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Estudiantes de posgrado vinculados con la Universidad",
                                            className="card-subtitle"),

                                    html.P(
                                        total_data_5,
                                        className="card-text",
                                        style={'textAlign': 'center'}
                                    ),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=3),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Suma de los reconocmientos económicos",
                                            className="card-subtitle"),

                                    html.P(
                                        total_data_6,
                                        className="card-text",
                                        style={'textAlign': 'center'}
                                    ),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=3),
                ]
            ),
        ]),
    html.H5('Estudiantes de pregrado vínculados con entidades externas'),
    dcc.Graph(id="graph_estudiantes_pregrado_entidades_externas",
              figure=px.bar(data_2,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'Estudiantes de pregrado'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "anio": True},
                            barmode="group"
                            )),
    html.H5('Estudiantes de posgrado vínculados con entidades externas'),
    dcc.Graph(id="graph_estudiantes_posgrado_entidades_externas",
              figure=px.bar(data_3,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'Estudiantes de posgrado'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "anio": True},
                            )),
    html.H5('Estudiantes de pregrado vinculados con la Universidad'),
    dcc.Graph(id="graph_estudiantes_pregrado_vinculados_unal",
              figure=px.bar(data_4,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'Estudiantes de pregrado'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "anio": True},
                            )),
    html.H5('Estudiantes de posgrado vinculados con la Universidad'),
    dcc.Graph(id="graph_estudiantes_posgrado_vinculados_unal",
              figure=px.bar(data_5,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'Estudiantes de posgrado'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "anio": True},
                            )),
    html.H5('Suma de los reconocmientos económicos'),
    dcc.Graph(id="graph_suma_reconocimientos_economicos",
              figure=px.bar(data_6,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'Reconocimientos económicos'
                            },
                            color_discrete_sequence=px.colors.qualitative.Plotly,
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
                            id="facultad_practicas_pasantias",
                            options=data['facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_practicas_pasantias",
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
                                id='logros_table_practicas_pasantias',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),

], className='layout')


@callback(
    Output("logros_table_practicas_pasantias", "data"),
    [Input("facultad_practicas_pasantias", "value"), Input("anio_practicas_pasantias", "value")])
def logros_alcanzados_practicas_pasantias(facultad, anio):
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