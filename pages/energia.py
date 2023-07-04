import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/energia')

data_2 = pd.read_excel(open(
    'pages/energia.xlsx', 'rb'), sheet_name='1')

data_3 = pd.read_excel(open(
    'pages/energia.xlsx', 'rb'), sheet_name='2')


# Consumo de energía en el último año

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
total_data_2 = f'{total_data_2:,}'.replace(',', ' ')

# Costo de energía en el último año

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
total_data_3 = f'{total_data_3:,}'.replace(',', ' ')
total_data_3 = '$ ' + total_data_3

layout = html.Div([
    html.H2('Gestión ambiental'),
    html.H3('Línea base antrópica'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Agua",
                                    href="/agua")),
            dbc.NavItem(dbc.NavLink("Energía", active=True,
                                    href="/energia")),
            dbc.NavItem(dbc.NavLink("Resíduos",
                                    href="/residuos")),
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
                                    html.H5(
                                        total_data_2,
                                        className="card-number",
                                    ),
                                    html.P("consumo de energía en (?)"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_data_3,
                                        className="card-number",
                                    ),
                                    html.P("costo de la energía"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.H5('Consumo de energía'),
    dcc.Graph(id="graph_consumo_energia",
              figure=px.bar(data_2,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'Consumo de energía'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "anio": True},
                            barmode="group"
                            )),
    html.H5('Costo de la energía'),
    dcc.Graph(id="graph_costo_energia",
              figure=px.bar(data_3,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'Costo de la energía'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "anio": True},
                            barmode="group"
                            )),
], className='layout')
