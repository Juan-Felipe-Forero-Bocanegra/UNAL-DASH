import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(__name__, path='/alianzas-redes-convenios-y-movilidad-de-investigacion')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Extensión, Innovación y Propiedad Intelectual&programa_param=Alianzas, redes, convenios y movilidades de investigación&actividad_param=Alianzas, redes, convenios y movilidades de investigación"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

list = []
list2 = []

for c in dataJson:
    if c['informeActividadDetalle']['orden'] == 1:
        i = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Logro': ''
                }
            if a['actividadDatoLista']['nombre'] == 'Logro' and a['actividadDatoLista']['orden'] == '1':
                o['Logro'] = a['cifra']
                i += 1
            if i == 1:
                list.append(o)
                i = 0
    if c['informeActividadDetalle']['orden'] == 2:
        o = {
                'Facultad':c['facultad'],
                'Año':c['anio'],
                'cifra': c['informeActividadDetalle']['cifra']
                }
        list2.append(o)

data = pd.DataFrame(list)
data_2 = pd.DataFrame(list2)

def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


layout = html.Div([])


# Nuevos convenios suscritos en el año

data_2["Año"] = data_2["Año"].astype('str')
data_2.fillna(0, inplace=True)
data_2['cifra'] = data_2['cifra'].astype('int')


data_2.apply(lambda x: total_function(x['Facultad'], x['Año'], data_2), axis=1)
total_data_2 = data_2['cifra'].sum()


layout = html.Div([
    html.H2('Extensión, Innovación y Propiedad Intelectual'),
    html.H3('Alianzas, redes, convenios y movilidades de investigación'),   
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
                                    html.P("convenios suscritos"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=3),
                ]
            ),
        ]),
    html.H5('Nuevos convenios suscritos'),
    dcc.Graph(id="graph_nuevos_convenios_suscritos",
              figure=px.bar(data_2,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Convenios suscritos'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Logros Alcanzados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_alianzas_redes_convenios",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_alianzas_redes_convenios",
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
                                id='logros_tabla_alianzas_redes_convenios',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_alianzas_redes_convenios", "data"),
    [Input("facultad_alianzas_redes_convenios", "value"), Input("anio_alianzas_redes_convenios", "value")])
def logros_alcanzados_alianzas_redes_convenios(facultad, anio):
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
