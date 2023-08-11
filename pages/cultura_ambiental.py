import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(__name__, path='/cultura-ambiental')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Gestión ambiental&programa_param=Programas transversales&actividad_param=Cultura ambiental"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

list = []
list2 = []
list3 = []
list4 = []

for c in dataJson:
    if c['informeActividadDetalle']['orden'] == 1:
        o = {
                'Facultad':c['facultad'],
                'Año':c['anio'],
                'cifra': c['informeActividadDetalle']['cifra']
                }
        list.append(o)
    if c['informeActividadDetalle']['orden'] == 2:
        o = {
                'Facultad':c['facultad'],
                'Año':c['anio'],
                'cifra': c['informeActividadDetalle']['cifra']
                }
        list2.append(o)
    if c['informeActividadDetalle']['orden'] == 3:
        o = {
                'Facultad':c['facultad'],
                'Año':c['anio'],
                'cifra': c['informeActividadDetalle']['cifra']
                }
        list3.append(o)
    if c['informeActividadDetalle']['orden'] == 4:
        o = {
                'Facultad':c['facultad'],
                'Año':c['anio'],
                'Gestión de residuos': c['informeActividadDetalle']['cifra']
                }
        list4.append(o)

data = pd.DataFrame(list4)
data_2 = pd.DataFrame(list)
data_3 = pd.DataFrame(list2)
data_4 = pd.DataFrame(list3)

def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# ¿La facultad cuenta con GAESO?

data_2["Año"] = data_2["Año"].astype(str)

data_2['cifra'] = data_2['cifra'].replace(['11'], 'Sí')
data_2['cifra'] = data_2['cifra'].replace(['12'], 'No')

gaeso_figure = px.scatter(data_2,
                          x="Año",
                          y="Facultad",
                          color="cifra",
                          labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'GAESO'
                          },
                          color_discrete_sequence=px.colors.qualitative.G10,
                          hover_data={
                              "cifra": True,
                              'Facultad': True,
                              "Año": True},
                          )
gaeso_figure.update_traces(marker_size=20)
gaeso_figure.update_xaxes(showgrid=True)
gaeso_figure.update_layout(xaxis_type='category')
gaeso_figure.update_xaxes(categoryorder='category ascending')
gaeso_figure.update_layout(scattermode="group")

# Número de asistentes a eventos ambientales

data_3["Año"] = data_3["Año"].astype('str')
data_3.fillna(0, inplace=True)
data_3['cifra'] = data_3['cifra'].astype('int')

data_3.apply(lambda x: total_function(x['Facultad'], x['Año'], data_3), axis=1)
total_data_3 = data_3['cifra'].sum()

# Número de eventos ambientales realizados

data_4["Año"] = data_4["Año"].astype('str')
data_4.fillna(0, inplace=True)
data_4['cifra'] = data_4['cifra'].astype('int')

data_4.apply(lambda x: total_function(x['Facultad'], x['Año'], data_4), axis=1)
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
                    ], className='card_container'), lg=4),
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
                    ], className='card_container'), lg=4),
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
                            y="Facultad",
                            color="Año",
                            labels={                                
                                'Facultad': 'Dependencia',
                                'cifra': 'Asistentes'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Eventos ambientales'),
    dcc.Graph(id="graph_eventos_ambientales_realizados",
              figure=px.bar(data_4,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={                                
                                'Facultad': 'Dependencia',
                                'cifra': 'Eventos'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
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
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_protocolo_directrices_ambientales",
                            options=data['Año'].unique(),
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
            df = df[df['Facultad'] == facultad]
            table = df.to_dict('records')
            return table
        if not facultad:
            df = data
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table
        if facultad and anio:
            df = data
            df = df[df['Facultad'] == facultad]
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table
    df = data
    table = df.to_dict('records')
    return table
