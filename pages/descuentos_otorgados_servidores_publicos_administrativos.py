import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(__name__, path='/descuentos-otorgados-servidores-publicos-administrativos')


f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Extensión, Innovación y Propiedad Intelectual&programa_param=Formación del personal docente y administrativo&actividad_param=Descuentos otorgados a los servidores públicos administrativos por concepto de capacitaciones ofrecidas por el área de extensión de la Facultad"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()


list2 = []
list3 = []

for c in dataJson:
    if c['informeActividadDetalle']['orden'] == 1:
        o = {
                'Facultad':c['facultad'],
                'Año':c['anio'],
                'cifra': c['informeActividadDetalle']['cifra']
                }
        list2.append(o)
    if c['informeActividadDetalle']['orden'] == 2:
        o = {
                'Facultad':c['facultad'],
                'Año':c['anio'],
                'cifra': c['informeActividadDetalle']['cifra']
                }
        list3.append(o)

data_2 = pd.DataFrame(list2)
data_3 = pd.DataFrame(list3)

def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# número de beneficiarios

data_2["Año"] = data_2["Año"].astype('str')
data_2.fillna(0, inplace=True)
data_2['cifra'] = data_2['cifra'].astype('int')

data_2.apply(lambda x: total_function(x['Facultad'], x['Año'], data_2), axis=1)
total_data_2 = data_2['cifra'].sum()

# valor total de los descuentos otorgados

data_3["Año"] = data_3["Año"].astype('str')
data_3.fillna(0, inplace=True)
data_3['cifra'] = data_3['cifra'].astype('float')

data_3.apply(lambda x: total_function(x['Facultad'], x['Año'], data_3), axis=1)
total_data_3 = data_3['cifra'].sum()
total_data_3 = f'{total_data_3:,}'.replace(',', ' ')
total_data_3 = '$ ' + total_data_3


layout = html.Div([
    html.H2('Extensión, Innovación y Propiedad Intelectual'),
    html.H3('Formación del personal docente y administrativo'),
     dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Fortalecimiento de competencias del personal", 
                                    href="/fortalecimiento-competencias-personal")),
            dbc.NavItem(dbc.NavLink("Descuentos a los servidores públicos administrativos en capacitaciones del área de extensión", active=True,
                                    href="/descuentos-otorgados-servidores-publicos-administrativos")),
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
                                    html.P("beneficiarios"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=3),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_data_3,
                                        className="card-number",
                                    ),
                                    html.P("total de los descuentos"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=3),
                ]
            ),
        ]),
    html.H5('Número de beneficiarios'),
    dcc.Graph(id="graph_numero_beneficiarios_descuentos",
              figure=px.bar(data_2,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Beneficiarios'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Valor total de los descuentos otorgados'),
    dcc.Graph(id="graph_valor_total_decuentos",
              figure=px.bar(data_3,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Valor total de los descuentos'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
], className='layout')


