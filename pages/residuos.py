import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/residuos')

data_2 = pd.read_excel(open(
    'pages/residuos.xlsx', 'rb'), sheet_name='1')

data_3 = pd.read_excel(open(
    'pages/residuos.xlsx', 'rb'), sheet_name='2')

data_4 = pd.read_excel(open(
    'pages/residuos.xlsx', 'rb'), sheet_name='3')

data_5 = pd.read_excel(open(
    'pages/residuos.xlsx', 'rb'), sheet_name='4')

data_6 = pd.read_excel(open(
    'pages/residuos.xlsx', 'rb'), sheet_name='5')

data_7 = pd.read_excel(open(
    'pages/residuos.xlsx', 'rb'), sheet_name='6')

data_8 = pd.read_excel(open(
    'pages/residuos.xlsx', 'rb'), sheet_name='7')

# Cantidad de residuos biodegradables

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

# Cantidad de residuos reciclables

data_3 = data_3.drop(
    columns=['area', 'programa', 'actividad', 'actividadDetalle'])

new_cols_3 = ['facultad', 'anio', 'cifra']
data_3 = data_3[new_cols_3]
data_3["anio"] = data_3["anio"].astype('str')
data_3.fillna(0, inplace=True)
data_3['cifra'] = data_3['cifra'].astype('int')


def total_function(facultad, anio):
    df_facultad = data_3[data_3['facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    data_3.loc[(data_3['facultad'] == facultad) & (
        data_3['anio'] == anio), 'total'] = df_total


data_3.apply(lambda x: total_function(x['facultad'], x['anio']), axis=1)
total_data_3 = data_3['cifra'].sum()

# Cantidad de residuos ordinarios

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

# Cantidad de RCD

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

# Cantidad de residuos químicos

data_6 = data_6.drop(
    columns=['area', 'programa', 'actividad', 'actividadDetalle'])

new_cols_6 = ['facultad', 'anio', 'cifra']
data_6 = data_6[new_cols_6]
data_6["anio"] = data_6["anio"].astype('str')
data_6.fillna(0, inplace=True)
data_6['cifra'] = data_6['cifra'].astype('int')


def total_function_6(facultad, anio):
    df_facultad = data_6[data_6['facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    data_6.loc[(data_6['facultad'] == facultad) & (
        data_6['anio'] == anio), 'total'] = df_total


data_6.apply(lambda x: total_function_6(x['facultad'], x['anio']), axis=1)
total_data_6 = data_6['cifra'].sum()

# Cantidad de residuos infecciosos

data_7 = data_7.drop(
    columns=['area', 'programa', 'actividad', 'actividadDetalle'])

new_cols_7 = ['facultad', 'anio', 'cifra']
data_7 = data_7[new_cols_7]
data_7["anio"] = data_7["anio"].astype('str')
data_7.fillna(0, inplace=True)
data_7['cifra'] = data_7['cifra'].astype('int')


def total_function_7(facultad, anio):
    df_facultad = data_7[data_7['facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    data_7.loc[(data_7['facultad'] == facultad) & (
        data_7['anio'] == anio), 'total'] = df_total


data_7.apply(lambda x: total_function_7(x['facultad'], x['anio']), axis=1)
total_data_7 = data_7['cifra'].sum()

# Cantidad de residuos posconsumo

data_8 = data_8.drop(
    columns=['area', 'programa', 'actividad', 'actividadDetalle'])

new_cols_8 = ['facultad', 'anio', 'cifra']
data_8 = data_8[new_cols_8]
data_8["anio"] = data_8["anio"].astype('str')
data_8.fillna(0, inplace=True)
data_8['cifra'] = data_8['cifra'].astype('int')


def total_function_8(facultad, anio):
    df_facultad = data_8[data_8['facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    data_8.loc[(data_8['facultad'] == facultad) & (
        data_8['anio'] == anio), 'total'] = df_total


data_8.apply(lambda x: total_function_8(x['facultad'], x['anio']), axis=1)
total_data_8 = data_8['cifra'].sum()

layout = html.Div([
    html.H2('Gestión ambiental'),
    html.H3('Línea base antrópica'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Agua",
                                    href="/agua")),
            dbc.NavItem(dbc.NavLink("Energia",
                                    href="/energia")),
            dbc.NavItem(dbc.NavLink("Residuos", active=True,
                                    href="/residuos")),
            dbc.NavItem(dbc.NavLink("Plagas y vectores", 
                                    href="/plagas-y-vectores")),
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
                                    html.H6("Residuos biodegradables",
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
                                    html.H6("Residuos reciclables",
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
                                    html.H6("Residuos ordinarios",
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
                                    html.H6("RCD generados",
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
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Residuos químicos",
                                            className="card-subtitle"),

                                    html.P(
                                        total_data_6,
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
                                    html.H6("Residuos infecciosos",
                                            className="card-subtitle"),

                                    html.P(
                                        total_data_7,
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
                                    html.H6("Residuos posconsumo",
                                            className="card-subtitle"),

                                    html.P(
                                        total_data_8,
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
    html.H5('Residuos biodegradables'),
    dcc.Graph(id="graph_residuos_biodegradables",
              figure=px.bar(data_2,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'Residuos biodegradables'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "anio": True},
                            barmode="group"
                            )),
    html.H5('Residuos reciclables'),
    dcc.Graph(id="graph_residuos_reciclabes",
              figure=px.bar(data_3,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'Residuos reciclables'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "anio": True},
                            barmode="group"
                            )),
    html.H5('Residuos ordinarios'),
    dcc.Graph(id="graph_residuos_ordinarios",
              figure=px.bar(data_4,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'Residuos ordinarios'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "anio": True},
                            barmode="group"
                            )),
    html.H5('RCD generado'),
    dcc.Graph(id="graph_RCD_generado",
              figure=px.bar(data_5,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'RDC generados'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "anio": True},
                            barmode="group"
                            )),
    html.H5('Residuos químicos'),
    dcc.Graph(id="graph_residuos_químicos",
              figure=px.bar(data_6,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'Resíduos químicos'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "anio": True},
                            barmode="group"
                            )),
    html.H5('Residuos infecciosos'),
    dcc.Graph(id="graph_residuos_infecciosos",
              figure=px.bar(data_7,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'Residuos infeccsiosos'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "anio": True},
                            barmode="group"
                            )),
    html.H5('Residuos posconsumo'),
    dcc.Graph(id="graph_residuos_posconsumo",
              figure=px.bar(data_8,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'Residuos posconsumo'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "anio": True},
                            barmode="group"
                            )),
], className='layout')
