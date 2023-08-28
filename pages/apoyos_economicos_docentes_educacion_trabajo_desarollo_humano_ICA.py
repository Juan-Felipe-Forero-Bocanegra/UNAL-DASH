import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(
    __name__, path='/apoyos-economicos-docentes-educacion-trabajo-desarrollo-humano-ICA')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Investigación y Creación Artística&programa_param=Despliegue de la investigación &actividad_param=Apoyos económicos otorgados a los docentes para financiar su participación en programas de educación formal, para el trabajo y el desarrollo humano o informal"
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
    if c['informeActividadDetalle']['orden'] == 2:
        o = {
            'Facultad': c['facultad'],
            'Año': c['anio'],
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


# Número de beneficiarios

data["Año"] = data["Año"].astype('str')
data.fillna(0, inplace=True)
data['cifra'] = data['cifra'].astype('int')

data.apply(lambda x: total_function(x['Facultad'], x['Año'], data), axis=1)
total_data = data['cifra'].sum()

# Valor total de los descuentos otorgados

data_2["Año"] = data_2["Año"].astype('str')
data_2.fillna(0, inplace=True)
data_2['cifra'] = data_2['cifra'].astype('float')

data_2.apply(lambda x: total_function(x['Facultad'], x['Año'], data_2), axis=1)
data_2['total'] = data_2['total'].map("{:,.2f}".format)
total_data_2 = data_2['cifra'].sum()
total_data_2 = f'{total_data_2:,}'.replace(',', ' ')
total_data_2 = '$ ' + total_data_2

layout = html.Div([
    html.H2('Investigación y Creación Artística'),
    html.H3('Despliegue de la investigación '),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink(
                "Semilleros de investigación", href="/semillero-investigacion-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Participación docente en la investigación", href="/participacion-docente-investigacion-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Apoyos económicos a los docentes (educación formal, trabajo y desarrollo humano)", active=True, href="/apoyos-economicos-docentes-educacion-trabajo-desarrollo-humano-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Grupos de investigación",  href="/grupos-investigacion-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Grupos de investigación por población",  href="/grupos-investigacion-poblacion-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Escuelas y centros de pensamiento y de excelencia",  href="/escuelas-centros-pensamiento-excelencia")),
            dbc.NavItem(dbc.NavLink(
                        "Internacionalización de la investigación", href="/internacionalizacion-investigacion-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Comités (Investigación, Ética)",  href="/comites-investigacion-etica-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Actualización de bases de datos (Hermes y otras)",  href="/actualizacion-bases-datos-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Articulación interistitucional", href="/articulacion-interinstitucional_ICA")),
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
                                        total_data,
                                        className="card-number",
                                    ),
                                    html.P("docentes beneficiados"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_data_2,
                                        className="card-number",
                                    ),
                                    html.P("valor total de los beneficios"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.H5('Número de beneficiarios'),
    dcc.Graph(id="graph_beneficiarios_apoyos_docentes_educacion_trabajo_desarrollo_humano_ICA",
              figure=px.bar(data,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Docentes beneficiados'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Valor total de los beneficios otorgados'),
    dcc.Graph(id="graph_valor_total_apoyos_docentes_educacion_trabajo_desarrollo_humano_ICA",
              figure=px.bar(data_2,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Valor de los apoyos económicos'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
], className='layout')
