import dash
from dash import html
import pandas as pd
import plotly.express as px
from dash import dcc, Input, Output, dash_table, ctx
import dash_bootstrap_components as dbc
import joblib

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

dropdown = html.Div(
    [
        dbc.Label(html.I("Seleccione que desea realizar"),
                  html_for="dropdown"),
        dcc.Dropdown(
            id="dropdown",
            options=[
                {"label": "Numero Compras", "value": 1},
                {"label": "Perfiles Compradores", "value": 2},
                {"label": "Aceptar Campaña", "value": 3},
                {"label": "Dinero Gastado", "value": 4}
            ],
            value=1
        ),
    ],
    className="mb-3",
)

sidebar = html.Div(
    [
        html.H2("LIMPIK ", className="display-4"),
        html.Hr(),
        html.P(
            "Prediga a partir de nuestro conjunto de datos cuales serian sus clientes potenciales", className="lead"
        ),
        dbc.Nav(
            [
                dropdown,
                dbc.NavLink("DATOS", href="/DATOS", active="exact"),
                dbc.NavLink("EDA", href="/EDA", active="exact"),
                dbc.NavLink("INFERENCIA", href="/INFERENCIA", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")],
              Input(component_id='dropdown',component_property="value"))
def render_page_content(pathname,dropdown):
    
    if dropdown == 1:
        return analytics_purchasing(pathname)
    elif dropdown == 2:
        return analytics_profiles(pathname)
    elif dropdown == 3:
        return analytics_campaign(pathname)
    elif dropdown == 4:
        return analytics_expenses(pathname)
    else:
        return html.Div(
        [
            html.H1("Error: Seleccione una acción", className="text-danger"),
            html.Hr(),
            html.P(f"Porfavor seleccione que desea realizar"),
        ],
        className="p-3 bg-light rounded-3",
    )


def analytics_purchasing(pathname):
    if pathname == "/DATOS":
        return "table compras"
    elif pathname == "/EDA":
        return "eda compras"
    elif pathname == "/INFERENCIA":
        return "inferencia compras"
    # If the user tries to reach a different page, return a 404 message
    return getDivError()

def analytics_profiles(pathname):
    if pathname == "/DATOS":
        return "table perfiles"
    elif pathname == "/EDA":
        return "eda perfiles"
    elif pathname == "/INFERENCIA":
        return "inferencia perfiles"
    # If the user tries to reach a different page, return a 404 message
    return getDivError()

def analytics_campaign(pathname):
    if pathname == "/DATOS":
        return "table campaña"
    elif pathname == "/EDA":
        return "eda campaña"
    elif pathname == "/INFERENCIA":
        return "inferencia campaña"
    # If the user tries to reach a different page, return a 404 message
    return getDivError()

def analytics_expenses(pathname):
    if pathname == "/DATOS":
        return "table gastos"
    elif pathname == "/EDA":
        return "eda gastos"
    elif pathname == "/INFERENCIA":
        return "inferencia gastos"
    # If the user tries to reach a different page, return a 404 message
    return getDivError()

def getDivError():
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )



if __name__ == '__main__':
    app.run_server(debug=True)
