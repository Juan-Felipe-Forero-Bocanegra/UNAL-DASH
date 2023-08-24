import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(__name__, path='/evaluacion-a-docentes')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Formación&programa_param=Formación del personal docente y administrativo&actividad_param=Evaluación a docentes"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

list = []
list2 = []
list3 = []

for c in dataJson:
    if c['informeActividadDetalle']['orden'] == 1:
        o = {
            'Facultad': c['facultad'],
            'Año': c['anio'],
            'cifra': c['informeActividadDetalle']['cifra']
        }
        list.append(o)
    if c['informeActividadDetalle']['orden'] == 2:
        i = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Elemento': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                o['Elemento'] = a['cifra']
                i += 1
            if i == 1:
                list2.append(o)
                i = 0
    if c['informeActividadDetalle']['orden'] == 3:
        i = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Elemento': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                o['Elemento'] = a['cifra']
                i += 1
            if i == 1:
                list3.append(o)
                i = 0


data = pd.DataFrame(list)
data_2 = pd.DataFrame(list2)
data_3 = pd.DataFrame(list3)


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# Calificación promedio

data["Año"] = data["Año"].astype('str')
data.fillna(0, inplace=True)
data['cifra'] = data['cifra'].astype('float')

data.apply(lambda x: total_function(x['Facultad'], x['Año'], data), axis=1)
total_data = data['cifra'].sum()


layout = html.Div([
    html.H2('Formación'),
    html.H3('Formación del personal docente y administrativo'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Fortalecimiento de competencias del personal",
                                    href="/fortalecimiento-competencias-personal-formacion")),
            dbc.NavItem(dbc.NavLink("Apoyos económicos a docentes en educación formal u informal",
                                    href="/apoyos-economicos-docentes-educacion-formal-u-informal")),
            dbc.NavItem(dbc.NavLink("Comisiones regulares para el personal docente",
                                    href="/comisiones-regulares-personal-docente")),
            dbc.NavItem(dbc.NavLink("Evaluación a docentes", active=True,
                                    href="/evaluacion-a-docentes")),
            dbc.NavItem(dbc.NavLink("Descuentos realizados a servidores públicos administrativos en matrículas",
                                    href="/descuentos-servidores-administrativos-matriculas-pregrado-posgrado")),

        ],
        pills=True),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_data,
                                        className="card-number",
                                    ),
                                    html.P("calificación promedio"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.H5('Calificación promedio de los docentes'),
    dcc.Graph(id="graph_calificacion_promedio_docentes",
              figure=px.bar(data,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Calificación promedio'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Elementos mejor calificados del personal docente'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_elementos_mejor_calificados_docentes",
                            options=data_2['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_elementos_mejor_calificados_docentes",
                            options=data_2['Año'].unique(),
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
                                id='logros_tabla_elementos_mejor_calificados_docentes',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),
    html.H5('Elementos peor calificados del personal docente'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_elementos_peor_calificados_docentes",
                            options=data_3['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_elementos_peor_calificados_docentes",
                            options=data_3['Año'].unique(),
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
                                id='logros_tabla_elementos_peor_calificados_docentes',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),
], className='layout')


@callback(
    Output("logros_tabla_elementos_mejor_calificados_docentes", "data"),
    [Input("facultad_elementos_mejor_calificados_docentes", "value"), Input("anio_elementos_mejor_calificados_docentes", "value")])
def logros_alcanzados_elementos_mejor_calificados_docentes(facultad, anio):
    if facultad or anio:
        if not anio:
            df = data_2
            df = df[df['Facultad'] == facultad]
            table = df.to_dict('records')
            return table
        if not facultad:
            df = data_2
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table
        if facultad and anio:
            df = data_2
            df = df[df['Facultad'] == facultad]
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table


@callback(
    Output("logros_tabla_elementos_peor_calificados_docentes", "data"),
    [Input("facultad_elementos_peor_calificados_docentes", "value"), Input("anio_elementos_peor_calificados_docentes", "value")])
def logros_alcanzados_elementos_peor_calificados_docentes(facultad, anio):
    if facultad or anio:
        if not anio:
            df = data_3
            df = df[df['Facultad'] == facultad]
            table = df.to_dict('records')
            return table
        if not facultad:
            df = data_3
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table
        if facultad and anio:
            df = data_3
            df = df[df['Facultad'] == facultad]
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table
