import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/convenios')

data = pd.read_excel('pages/convenios.xlsx')

data = data.drop(columns=['area','programa','actividad', 'actividadDetalle'])
data = data.iloc[1:]

new_cols = ["facultad","anio","Área","Tipo",'Entidades', 'Logro']
data=data[new_cols]

layout = html.Div([ 
    html.Br(), 
    html.H2('Relaciones Interinstitucionales'),
    html.Br(), 
    html.H3('Convenios'),
    html.Br(), 
    dcc.Dropdown(
        id="facultad",
        options= data['facultad'].unique(),
        clearable=True,
        placeholder="Seleccione la facultad",
    ),
    dcc.Dropdown(
        id="anio",
        options= data['anio'].unique(),
        clearable=True,
        placeholder="Seleccione el año",
    ),
    dcc.Dropdown(
        id="Área",
        options= data['Área'].unique(),
        clearable=True,
        placeholder="Seleccione el área",
    ),
    html.Br(),         
    dash_table.DataTable(
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        },
        id = 'convenios'
    )
])


@callback(
    Output("convenios", "data"), 
    [Input("facultad", "value"), Input("anio", "value"), Input("Área", "value")])
def convenios(facultad, anio, area):
    if area or anio or facultad:
        if not anio and not facultad:
            df = data
            df = df[df['Área'] == area]
            table = df.to_dict('records')
            return table
        if not area and not facultad:
            df = data
            df = df[df['anio'] == anio]
            table = df.to_dict('records')
            return table
        if not area and not anio:
            df = data
            df = df[df['facultad'] == facultad]
            table = df.to_dict('records')
            return table
        if facultad and area and not anio:
            df = data
            df = df[df['facultad'] == facultad]
            df = df[df['Área'] == area]
            table = df.to_dict('records')
            return table
        if facultad and anio and not area:
            df = data
            df = df[df['facultad'] == facultad]
            df = df[df['anio'] == anio]
            table = df.to_dict('records')
            return table    
        if area and anio and not facultad:
            df = data
            df = df[df['Área'] == area]
            df = df[df['anio'] == anio]
            table = df.to_dict('records')
            return table
        if facultad and area and anio:
            df = data
            df = df[df['facultad'] == facultad]
            df = df[df['Área'] == area]
            df = df[df['anio'] == anio]
            table = df.to_dict('records')
            return table 
    df = data
    table = df.to_dict('records')
    return table

