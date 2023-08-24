import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(
    __name__, path='/apoyos-economicos-docentes-educacion-formal-u-informal')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Formación&programa_param=Formación del personal docente y administrativo&actividad_param=Apoyos económicos otorgados a los docentes para financiar su participación en programas de educación formal, para el trabajo y el desarrollo humano o informal"
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
    html.H2('Formación'),
    html.H3('Formación del personal docente y administrativo'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Fortalecimiento de competencias del personal",
                                    href="/fortalecimiento-competencias-personal-formacion")),
            dbc.NavItem(dbc.NavLink("Apoyos económicos a docentes en educación formal u informal", active=True,
                                    href="/apoyos-economicos-docentes-educacion-formal-u-informal")),
            dbc.NavItem(dbc.NavLink("Comisiones regulares para el personal docente",
                                    href="/comisiones-regulares-personal-docente")),
            dbc.NavItem(dbc.NavLink("Evaluación a docentes",
                                    href="/evaluacion-a-docentes")),
            dbc.NavItem(dbc.NavLink("Descuentos realizados a servidores públicos administrativos en matrículas",
                                    href="/descuentos-servidores-administrativos-matriculas-pregrado-posgrado")),
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
                                    html.P("beneficiados"),
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
                                    html.P("valor total de los descuentos"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.H5('Número de beneficiarios'),
    dcc.Graph(id="graph_numero_beneficiarios_apoyos_docentes_educacion_formal_u_informal",
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
    html.H5('Valor total de los descuentos otorgados'),
    dcc.Graph(id="graph_valor_total_descuentos_apoyos_docentes_educacion_formal_u_informal",
              figure=px.bar(data_2,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Valor de los descuentos'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
], className='layout')
