import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(__name__, path='/graduacion-asuntos-estudiantiles')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Formación&programa_param=Asuntos estudiantiles&actividad_param=Graduación"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

list = []
list2 = []

for c in dataJson:
    if c['informeActividadDetalle']['orden'] == 1:
        o = {
            'Facultad': c['facultad'],
            'Año': c['anio'],
            'cifra': c['informeActividadDetalle']['cifra']
        }
        list.append(o)

data_2 = pd.DataFrame(list)


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# Exención de derechos académicos por créditos de pregrado o beca*

data_2["Año"] = data_2["Año"].astype('str')
data_2.fillna(0, inplace=True)
data_2['cifra'] = data_2['cifra'].astype('int')

data_2.apply(lambda x: total_function(x['Facultad'], x['Año'], data_2), axis=1)
total_data_2 = data_2['cifra'].sum()

layout = html.Div([
    html.H2('Formación'),
    html.H3('Asuntos estudiantiles'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Ingreso",
                                    href="/ingreso-asuntos-estudiantiles")),
            dbc.NavItem(dbc.NavLink("Asignaturas",
                                    href="/asignaturas-asuntos-estudiantiles")),
            dbc.NavItem(dbc.NavLink("Semestre",
                                    href="/semestre-asuntos-estudiantiles")),
            dbc.NavItem(dbc.NavLink("Tesis",
                                    href="/tesis-trabajo-final-asuntos-estudiantiles")),
            dbc.NavItem(dbc.NavLink("Graduación", active=True,
                                    href="/graduacion-asuntos-estudiantiles")),
            dbc.NavItem(dbc.NavLink("Otros",
                                    href="/otros-asuntos-estudiantiles")),
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
                                    html.P(
                                        "exención de derechos académicos por créditos de pregrado o beca"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.H5('Exención de derechos académicos por créditos de pregrado o beca'),
    dcc.Graph(id="graph_exencion_derechos_asuntos_estudiantiles",
              figure=px.bar(data_2,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Exención de derechos académicos'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
], className='layout')
