import dash
from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import requests
import json
import time
from flask import session

url = "http://localhost:8070/authenticate"
data = {'username': 'jforerobo', 'password': 'T$Cc#s7%hPqk'}
headers = {'Content-type': 'application/json'}
r = requests.post(url, json=data)
jsonResponse = r.json()
token = 'Bearer ' + jsonResponse['token']
text_file = open("file.txt", "w")
n = text_file.write(token)
text_file.close()


app = Dash(__name__, use_pages=True)
server = app.server


app.layout = html.Div([
    dcc.Interval(
        id='interval',
        interval=1 * 3600000,
        n_intervals=0),
    dcc.Store(id='store'),
    dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Convenios", href='/convenios'),
                    dbc.DropdownMenuItem('Movilidad académica',
                                         href="/movilidad-estudiantil"),
                ],
                nav=True,
                in_navbar=True,
                label="Relaciones interinstitucionales",
            ),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem(
                        "Proyectos de extensión", href='/presentacion-propuestas-y-cotizaciones-de-estudios'),
                    dbc.DropdownMenuItem(
                        "Alianzas, redes, convenios", href='/alianzas-redes-convenios-y-movilidad-de-investigacion'),
                    dbc.DropdownMenuItem(
                        "Estrategia de comunicación de la Extensión", href='/estrategia-comunicacion-extension'),
                    dbc.DropdownMenuItem(
                        "Innovaciones", href='/innovaciones'),
                    dbc.DropdownMenuItem(
                        "Reconocimiento y visibilidad de la UNAL", href='/reconocimiento-visibilidad-universidad'),
                    dbc.DropdownMenuItem(
                        "Prácticas y pasantías", href='/practicas-y-pasantias'),
                    dbc.DropdownMenuItem(
                        "Formación del personal", href='/fortalecimiento-competencias-personal'),
                ],
                nav=True,
                in_navbar=True,
                label="Extensión, Innovación y Propiedad Intelectual",
            ),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem(
                        "Consolidación de la paz", href='/formacion-paz'),
                ],
                nav=True,
                in_navbar=True,
                label="Paz y ética",
            ),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Línea base antrópica", href='/agua'),
                    dbc.DropdownMenuItem(
                        "Programas transversales", href='/alertas-tempranas'),
                ],
                nav=True,
                in_navbar=True,
                label="Gestión ambiental",
            ),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Producción editorial", href='/'),
                    dbc.DropdownMenuItem(
                        "Difusión y comercialización", href='/difusion-comercializacion-publicaciones'),
                ],
                nav=True,
                in_navbar=True,
                label="Divulgación de la producción académica",
            ),
            dbc.NavItem(dbc.NavLink("Gobierno de TI",
                        href='/repositorios-informacion')),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Gestión de programas curriculares",
                                         href='/creacion-modicacion-programas-planes-estudio'),
                    dbc.DropdownMenuItem("Cupos", href='/oferta-cupos'),
                    dbc.DropdownMenuItem(
                        "Cursos y asignaturas", href='/cursos'),
                    dbc.DropdownMenuItem(
                        "Gestión de la actividad académica", href='/catedras-sede'),
                    dbc.DropdownMenuItem(
                        "Tutores docentes", href='/designacion-tutores-docentes'),
                    dbc.DropdownMenuItem(
                        "Reconocimientos económicos a estudiantes", href='/beca-auxiliar-docente'),
                    dbc.DropdownMenuItem(
                        "Acompañamiento estudiantil ", href='/acompanamiento-programas-especiales'),
                    dbc.DropdownMenuItem("Formación del personal docente y administrativo",
                                         href='/fortalecimiento-competencias-personal-formacion'),
                    dbc.DropdownMenuItem("Apoyo a la Innovación Académica",
                                         href='/liderazgo-emprendimiento-empleabilidad'),
                    dbc.DropdownMenuItem("Asuntos estudiantiles",
                                         href='/ingreso-asuntos-estudiantiles'),
                ],
                nav=True,
                in_navbar=True,
                label="Formación",
            ),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Actividades de fomento y fortalecimiento",
                                         href='/capacitaciones-investigacion-creacion-artistica'),
                    dbc.DropdownMenuItem("Convocatorias",
                                         href='/convocatorias-internas-institucionales'),
                    dbc.DropdownMenuItem("Proyectos de investigación",
                                         href='/cifras-proyectos-periodo'),
                    dbc.DropdownMenuItem("Alianzas, redes, convenios y movilidades",
                                         href='/alianzas-redes-convenios-ICA'),
                    dbc.DropdownMenuItem("Movilidad investigativa",
                                         href='/movilidad-estudiantil-investigativa-ICA'),
                    dbc.DropdownMenuItem("Innovación",
                                         href='/actividades-innovacion-ICA'),
                    dbc.DropdownMenuItem("Despliegue de la investigación",
                                         href='/semillero-investigacion-ICA'),

                ],
                nav=True,
                in_navbar=True,
                label="Investigación y Creación Artística",
            ),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem(
                        "Planeación táctica y operativa del SNL", href='/programas-planes-proyectos-laboratorios'),
                    dbc.DropdownMenuItem(
                        "Proyectos de laboratorios", href='/formulacion-ejecucion-proyectos-y-convenios-laboratorios'),
                    dbc.DropdownMenuItem(
                        "Alianzas, convenios o donaciones", href='/alianzas-convenios-donaciones-laboratorios'),
                    dbc.DropdownMenuItem(
                        "Servicios prestados en los laboratorios", href='/servicios-extension-laboratorios'),
                    dbc.DropdownMenuItem(
                        "Cifras SNIES", href='/cifras-snies-laboratorios'),
                    dbc.DropdownMenuItem(
                        "Actualizacion HERMES", href='/actualizacion-hermes-laboratorios'),
                ],
                nav=True,
                in_navbar=True,
                label="Gestión de laboratorios",
            ),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem(
                        "Coordinación del Bienestar Universitario", href='/proyectos-sistema-bienestar-universitario'),
                    dbc.DropdownMenuItem(
                        "Área de Acompañamiento Integral", href='/admision-e-induccion-bienestar-universitario'),
                    dbc.DropdownMenuItem(
                        "Área de Gestión y Fomento Socioeconómico", href='/apoyos-socioeconomicos-estudiantes-bienestar-universitario'),
                    dbc.DropdownMenuItem(
                        "Área de Salud", href='/logros-actividades-areas-salud-bienestar-universitario'),
                    dbc.DropdownMenuItem(
                        "Área de Cultura", href='/eventos-culturales-artistico-bienestar-universitario'),
                    dbc.DropdownMenuItem(
                        "Área de Actividad Física y Deporte", href='/eventos-deportivos-bienestar-universitario'),

                    dbc.DropdownMenuItem(
                        "Programa de egresados", href='/actividades-egresados-bienestar-universitario'),
                    dbc.DropdownMenuItem(
                        "La movilidad como apoyo de bienestar", href='/movilidad-estudiantil-bienestar-universitario'),
                ],
                nav=True,
                in_navbar=True,
                label="Bienestar universitario",
            ),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem(
                        "Divulgación general", href='/contenidos-produccion-publicacion-divulgacion-comunicacion'),
                    dbc.DropdownMenuItem(
                        "Divulgación oficial (normatividad)", href='/mecanismo-comunicacion-informacion-oficial'),
                    dbc.DropdownMenuItem(
                        "Atención a PQRS", href='/atencion-PQRS-comunicacion'),
                ],
                nav=True,
                in_navbar=True,
                label="Comunicación",
            ),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem(
                        "Implementación del Sistema de Gestión de Calidad", href='/procesos-y-procedimientos-desarrollo-organizacional'),
                ],
                nav=True,
                in_navbar=True,
                label="Desarrollo Organizacional",
            ),



        ],
        brand="Prig Data App",
        color="light",
        dark=False,
        expand="xs"
    ),

    dash.page_container
])


@callback(
    Output("store", "data"),
    Input('interval', 'n_intervals')
)
def login(interval):
    url = "http://localhost:8070/authenticate"
    data = {'username': 'jforerobo', 'password': 'T$Cc#s7%hPqk'}
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, json=data)
    jsonResponse = r.json()
    token = 'Bearer ' + jsonResponse['token']
    text_file = open("file.txt", "w")
    n = text_file.write(token)
    text_file.close()
    return {'token': token}


if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
