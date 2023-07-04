import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/cultura-ambiental')

data = pd.read_excel(open(
    'pages/cultura_ambiental.xlsx', 'rb'), sheet_name='4')

data_2 = pd.read_excel(open(
    'pages/cultura_ambiental.xlsx', 'rb'), sheet_name='1')

data_3 = pd.read_excel(open(
    'pages/cultura_ambiental.xlsx', 'rb'), sheet_name='2')

data_4 = pd.read_excel(open(
    'pages/cultura_ambiental.xlsx', 'rb'), sheet_name='3')

# Protocolos y directrices ambientales utilizados con frecuencia
data = data.drop(columns=['area', 'programa', 'actividad', 'actividadDetalle'])

new_cols = ['facultad', 'anio', 'Protocolo']
data = data[new_cols]

# ¿La facultad cuenta con GAESO?

data_2 = data_2.drop(
    columns=['area', 'programa', 'actividad', 'actividadDetalle'])

new_cols_2 = ['facultad', 'anio', 'cifra']
data_2 = data_2[new_cols_2]
data_2["anio"] = data_2["anio"].astype(str)

gaeso_figure = px.scatter(data_2,
                          x="anio",
                          y="facultad",
                          color="cifra",
                          labels={
                                'anio': 'Año',
                                'facultad': 'Dependencia',
                                'cifra': 'GAESO'
                          },
                          color_discrete_sequence=px.colors.qualitative.G10,
                          hover_data={
                              "cifra": True,
                              'facultad': True,
                              "anio": True},
                          )
gaeso_figure.update_traces(marker_size=20)
gaeso_figure.update_xaxes(showgrid=True)
gaeso_figure.update_layout(xaxis_type='category')
gaeso_figure.update_xaxes(categoryorder='category ascending')
gaeso_figure.update_layout(scattermode="group")

# Número de asistentes a eventos ambientales

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

# Número de eventos ambientales realizados

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

layout = html.Div([
    html.H2('Gestión ambiental'),
    html.H3('Programas transversales'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Alertas tempranas",
                                    href="/alertas-tempranas")),
            dbc.NavItem(dbc.NavLink("Riesgos ambientales",
                                    href="/riesgos-ambientales")),
            dbc.NavItem(dbc.NavLink("Cultura ambiental", active=True,
                                    href="/cultura-ambiental")),
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
                                        total_data_3,
                                        className="card-number",
                                    ),
                                    html.P("asistentes a eventos ambientales"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=3),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_data_4,
                                        className="card-number",
                                    ),
                                    html.P("eventos realizados"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=3),
                ]
            ),
        ]),
    html.H5('GAESO'),
    dcc.Graph(id="graph_gaeso",
              figure=gaeso_figure),
    html.H5('Asistentes a eventos ambientales'),
    dcc.Graph(id="graph_asistentes_eventos_ambientales",
              figure=px.bar(data_3,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'Asistentes'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "anio": True},
                            barmode="group"
                            )),
    html.H5('Eventos ambientales'),
    dcc.Graph(id="graph_eventos_ambientales_realizados",
              figure=px.bar(data_4,
                            x="cifra",
                            y="facultad",
                            color="anio",
                            labels={
                                'anio': 'año',
                                'facultad': 'Dependencia',
                                'cifra': 'Eventos'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "anio": True},
                            barmode="group"
                            )),
    html.H5('Protocolos y directrices ambientales'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_protocolo_directrices_ambientales",
                            options=data['facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_protocolo_directrices_ambientales",
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
                                id='logros_tabla_protocolo_directrices_ambientales',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),
], className='layout')


@callback(
    Output("logros_tabla_protocolo_directrices_ambientales", "data"),
    [Input("facultad_protocolo_directrices_ambientales", "value"), Input("anio_protocolo_directrices_ambientales", "value")])
def logros_alcanzados_protocolo_directrices_ambientales(facultad, anio):
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
