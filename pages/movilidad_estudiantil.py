import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
from flask import session
import requests
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/movilidad-estudiantil')
# server = app.server

# data = pd.read_excel('pages/movilidad_estudiantil_2.xlsx')
# data_2 = pd.read_excel('pages/logros.xlsx')

f = open("file.txt", "r")
token = f.readline()
url = "http://localhost:8070/reporte_cifras/buscarCifras?area_param=Relaciones Interinstitucionales&programa_param=Movilidad académica&actividad_param=Movilidad estudiantil"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

# ESTUDIANTES BENEFICIADOS

list = []

for c in dataJson:
    if c['informeActividadDetalle']['nombre'] == 'Estudiantes beneficiados':
        i = 0
        j = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Estudiantes beneficiados': '',
                    'Tipo': '',
                    'Nivel': ''
                }
            if a['actividadDatoLista']['nombre'] == 'Estudiantes beneficiados' and a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Estudiantes beneficiados'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['nombre'] == 'Tipo' and a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Tipo'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['nombre'] == 'Nivel' and a['actividadDatoLista']['orden'] == '3':
                if a['indice'] == j:
                    o['Nivel'] = a['cifra']
                    i += 1
            if i == 3:
                list.append(o)
                i = 0
                j += 1

df = pd.DataFrame(list)
df['Nivel'] = df['Nivel'].replace(['556'], 'Nacional')
df['Nivel'] = df['Nivel'].replace(['557'], 'Internacional')
df['Tipo'] = df['Tipo'].replace(['553'], 'Movilidad entrante')
df['Tipo'] = df['Tipo'].replace(['554'], 'Movilidad saliente')
data = df

data["Año"] = data["Año"].astype('str')
data['Estudiantes beneficiados'] = data['Estudiantes beneficiados'].astype(int)

# movilidad estudiantil nacional
movilidad_estudiantil_nacional = data[data['Nivel'] == 'Nacional']

# movilidad estudiantil nacional entrante
movilidad_estudiantil_nacional_entrante = movilidad_estudiantil_nacional[movilidad_estudiantil_nacional['Tipo']  == 'Movilidad entrante']
movilidad_estudiantil_nacional_entrante = movilidad_estudiantil_nacional_entrante.sort_values('Facultad', ascending=False)
total_movilidad_estudiantil_nacional_entrante = movilidad_estudiantil_nacional_entrante['Estudiantes beneficiados'].sum()
print('movilidad_estudiantil_nacional_entrante_sort')
print(total_movilidad_estudiantil_nacional_entrante)

# movilidad estudiantil nacional saliente
movilidad_estudiantil_nacional_saliente = movilidad_estudiantil_nacional[movilidad_estudiantil_nacional['Tipo']
                                                                         == 'Movilidad saliente']
movilidad_estudiantil_nacional_saliente = movilidad_estudiantil_nacional_saliente.sort_values(
    'Facultad', ascending=False)
total_movilidad_estudiantil_nacional_saliente = movilidad_estudiantil_nacional_saliente['Estudiantes beneficiados'].sum(
)

# movilidad estudiantil internacional
movilidad_estudiantil_internacional = data[data['Nivel'] == 'Internacional']
# movilidad estudiantil internacional entrante
movilidad_estudiantil_internacional_entrante = movilidad_estudiantil_internacional[
    movilidad_estudiantil_internacional['Tipo'] == 'Movilidad entrante']
movilidad_estudiantil_internacional_entrante = movilidad_estudiantil_internacional_entrante.sort_values(
    'Facultad', ascending=False)
total_movilidad_estudiantil_internacional_entrante = movilidad_estudiantil_internacional_entrante['Estudiantes beneficiados'].sum(
)

# movilidad estudiantil internacional saliente
movilidad_estudiantil_internacional_saliente = movilidad_estudiantil_internacional[
    movilidad_estudiantil_internacional['Tipo'] == 'Movilidad saliente']
movilidad_estudiantil_internacional_saliente = movilidad_estudiantil_internacional_saliente.sort_values(
    'Facultad', ascending=False)
total_movilidad_estudiantil_internacional_saliente = movilidad_estudiantil_internacional_saliente['Estudiantes beneficiados'].sum(
)

# LOGROS ALCANZADOS
list_2 = []
for c in dataJson:
    if c['informeActividadDetalle']['nombre'] == 'Logros alcanzados':
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
                list_2.append(o)
                i = 0

df_logros = pd.DataFrame(list_2)
data_2 = df_logros
print(data_2.head())

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
    html.P(id='service_output_movilidad_academica'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_movilidad_estudiantil_nacional_entrante,
                                        className="card-number",
                                    ),
                                    html.P("movilidad nacional entrante"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_movilidad_estudiantil_nacional_saliente,
                                        className="card-number",
                                    ),
                                    html.P("movilidad nacional saliente"),
                                ]
                            ),
                            style={"width": "18rem"},
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_movilidad_estudiantil_internacional_entrante,
                                        className="card-number",
                                    ),
                                    html.P("movilidad internacional entrante"),
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
                                    html.H5(
                                        total_movilidad_estudiantil_internacional_saliente,
                                        className="card-number",
                                    ),
                                    html.P("movilidad internacional saliente"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.H5('Movilidad nacional entrante'),
    dcc.Graph(id="graph_movilidad_estudiantil_nacional_entrante",
              figure=px.bar(movilidad_estudiantil_nacional_entrante,
                            x="Estudiantes beneficiados",
                            y="Facultad",
                            color="Año",
                            labels={
                                'facultad': 'Dependencia',
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "Estudiantes beneficiados": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Movilidad nacional saliente'),
    dcc.Graph(id="graph_movilidad_estudiantil_nacional_saliente",
              figure=px.bar(movilidad_estudiantil_nacional_saliente,
                            x="Estudiantes beneficiados",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "Estudiantes beneficiados": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Movilidad internacional entrante'),
    dcc.Graph(id="graph_movilidad_estudiantil_internacional_entrante",
              figure=px.bar(movilidad_estudiantil_internacional_entrante,
                            x="Estudiantes beneficiados",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "Estudiantes beneficiados": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Movilidad internacional saliente'),
    dcc.Graph(id="graph_movilidad_estudiantil_internacional_saliente",
              figure=px.bar(movilidad_estudiantil_internacional_saliente,
                            x="Estudiantes beneficiados",
                            y="Facultad",
                            color="Año",
                            labels={
                                'facultad': 'Dependencia'},
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "Estudiantes beneficiados": True,
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
                            id="facultad_movilidad_estudiantil",
                            options=data_2['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_movilidad_estudiantil",
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
            df = df[df['Facultad'] == facultad]
            data = df.to_dict('records')
            return data
        if not facultad:
            df = data_2
            df = df[df['Año'] == anio]
            data = df.to_dict('records')
            return data
        if facultad and anio:
            df = data_2
            df = df[df['Facultad'] == facultad]
            df = df[df['Año'] == anio]
            data = df.to_dict('records')
            return data
    df = data_2
    data = df.to_dict('records')
    return data
