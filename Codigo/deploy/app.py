import dash
from dash import html
import pandas as pd
import plotly.express as px
from dash import dcc, Input, Output, dash_table, ctx
import dash_bootstrap_components as dbc
import joblib

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv("../../datos/clean_marketing_campaing.csv")

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
                #dbc.NavLink("EDA", href="/EDA", active="exact"),
                dbc.NavLink("INFERENCIA", href="/INFERENCIA", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

inferenciaTarget1 = html.Div([
        html.Div([
            html.H1("COMPRAS POR CATALOGO")
        ],style={"background-image":"https://img.freepik.com/vector-premium/tienda-productos-organicos-supermercado_182089-263.jpg?w=2000"}),
        html.Div([
            html.Div([
                dbc.Label("Gastos en vinos", html_for="mntWinesCatalog"),
                dbc.Input(type="text", id="mntWinesCatalog", placeholder="Ingrese el monto del gasto en vinos")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Gasto en carnes", html_for="mntMeatProductsCatalog"),
                dbc.Input(type="text", id="mntMeatProductsCatalog", placeholder="Ingrese el monto del gasto en carnes")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Ingresos", html_for="incomeCatalog"),
                dbc.Input(type="text", id="incomeCatalog", placeholder="Ingrese los ingresos mensuales")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Compras por tienda fisica", html_for="numStorePurchasesCatalog"),
                dbc.Input(type="text", id="numStorePurchasesCatalog", placeholder="Ingrese la cantidad de compras realizadas por tienda fisica")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Gasto en productos premium", html_for="mntGoldProdsCatalog"),
                dbc.Input(type="text", id="mntGoldProdsCatalog", placeholder="Ingrese el monto del gasto en productos premium")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Gasto en frutas", html_for="mntFruitsCatalog"),
                dbc.Input(type="text", id="mntFruitsCatalog", placeholder="Ingrese el monto del gasto en frutas")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Gasto en pescado", html_for="mntFishProductsCatalog"),
                dbc.Input(type="text", id="mntFishProductsCatalog", placeholder="Ingrese el monto del gasto en productos de pescado")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Gasto en dulces", html_for="mntSweetProductsCatalog"),
                dbc.Input(type="text", id="mntSweetProductsCatalog", placeholder="Ingrese el monto del gasto en productos dulces")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Compras por pagina web", html_for="numWebPurchasesCatalog"),
                dbc.Input(type="text", id="numWebPurchasesCatalog", placeholder="Ingrese la cantidad de compras realizadas por pagina web")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Niños en casa", html_for="kidhomeCatalog"),
                dbc.Input(type="text", id="kidhomeCatalog", placeholder="Ingrese la cantidad de niños del hogar")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Visitas web", html_for="numWebVisitsMonthCatalog"),
                dbc.Input(type="text", id="numWebVisitsMonthCatalog", placeholder="Ingrese la cantidad de visitas web por mes")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Button("Predecir compras por catalogo", id="submitCatalog", n_clicks=0, color="secondary", className="me-1")
            ], style={"padding-top": "20px"}),
            html.Div([

            ], id="div-response-catalog", style={"padding-top": "20px"}),
            html.Hr()
        ]),


        html.Div([
            html.H1("COMPRAS POR PAGINA WEB")
        ],),
        html.Div([
            html.Div([
                dbc.Label("Compras por catalogo", html_for="numCatalogPurchasesWeb"),
                dbc.Input(type="text", id="numCatalogPurchasesWeb", placeholder="Ingrese la cantidad de compras realizadas por catalogo")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Gastos en vinos", html_for="mntWinesWeb"),
                dbc.Input(type="text", id="mntWinesWeb", placeholder="Ingrese el monto del gasto en vinos")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Gasto en carnes", html_for="mntMeatProductsWeb"),
                dbc.Input(type="text", id="mntMeatProductsWeb", placeholder="Ingrese el monto del gasto en carnes")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Ingresos", html_for="incomeWeb"),
                dbc.Input(type="text", id="incomeWeb", placeholder="Ingrese los ingresos mensuales")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Compras por tienda fisica", html_for="numStorePurchasesWeb"),
                dbc.Input(type="text", id="numStorePurchasesWeb", placeholder="Ingrese la cantidad de compras realizadas por tienda fisica")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Gasto en pescado", html_for="mntFishProductsWeb"),
                dbc.Input(type="text", id="mntFishProductsWeb", placeholder="Ingrese el monto del gasto en productos de pescado")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Gasto en productos premium", html_for="mntGoldProdsWeb"),
                dbc.Input(type="text", id="mntGoldProdsWeb", placeholder="Ingrese el monto del gasto en productos premium")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Gasto en frutas", html_for="mntFruitsWeb"),
                dbc.Input(type="text", id="mntFruitsWeb", placeholder="Ingrese el monto del gasto en frutas")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Gasto en dulces", html_for="mntSweetProductsWeb"),
                dbc.Input(type="text", id="mntSweetProductsWeb", placeholder="Ingrese el monto del gasto en productos dulces")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Niños en casa", html_for="kidhomeWeb"),
                dbc.Input(type="text", id="kidhomeWeb", placeholder="Ingrese la cantidad de niños del hogar")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Visitas web", html_for="numWebVisitsMonthWeb"),
                dbc.Input(type="text", id="numWebVisitsMonthWeb", placeholder="Ingrese la cantidad de visitas web por mes")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Button("Predecir compras por pagina web", id="submitWeb", n_clicks=0, color="secondary", className="me-1")
            ], style={"padding-top": "20px"}),
            html.Div([

            ], id="div-response-web", style={"padding-top": "20px"}),
            html.Hr()
        ]),


        html.Div([
            html.H1("COMPRAS POR TIENDA FISICA")
        ],),
        html.Div([
            html.Div([
                dbc.Label("Compras por catalogo", html_for="numCatalogPurchasesStore"),
                dbc.Input(type="text", id="numCatalogPurchasesStore", placeholder="Ingrese la cantidad de compras realizadas por catalogo")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Gastos en vinos", html_for="mntWinesStore"),
                dbc.Input(type="text", id="mntWinesStore", placeholder="Ingrese el monto del gasto en vinos")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Gasto en carnes", html_for="mntMeatProductsStore"),
                dbc.Input(type="text", id="mntMeatProductsStore", placeholder="Ingrese el monto del gasto en carnes")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Ingresos", html_for="incomeStore"),
                dbc.Input(type="text", id="incomeStore", placeholder="Ingrese los ingresos mensuales")
            ], style={"padding-top": "20px"}),
             html.Div([
                dbc.Label("Gasto en pescado", html_for="mntFishProductsStore"),
                dbc.Input(type="text", id="mntFishProductsStore", placeholder="Ingrese el monto del gasto en productos de pescado")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Gasto en frutas", html_for="mntFruitsStore"),
                dbc.Input(type="text", id="mntFruitsStore", placeholder="Ingrese el monto del gasto en frutas")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Gasto en productos premium", html_for="mntGoldProdsStore"),
                dbc.Input(type="text", id="mntGoldProdsStore", placeholder="Ingrese el monto del gasto en productos premium")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Gasto en dulces", html_for="mntSweetProductsStore"),
                dbc.Input(type="text", id="mntSweetProductsStore", placeholder="Ingrese el monto del gasto en productos dulces")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Compras por pagina web", html_for="numWebPurchasesStore"),
                dbc.Input(type="text", id="numWebPurchasesStore", placeholder="Ingrese la cantidad de compras realizadas por pagina web")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Niños en casa", html_for="kidhomeStore"),
                dbc.Input(type="text", id="kidhomeStore", placeholder="Ingrese la cantidad de niños del hogar")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Label("Visitas web", html_for="numWebVisitsMonthStore"),
                dbc.Input(type="text", id="numWebVisitsMonthStore", placeholder="Ingrese la cantidad de visitas web por mes")
            ], style={"padding-top": "20px"}),
            html.Div([
                dbc.Button("Predecir compras por tienda fisica", id="submitStore", n_clicks=0, color="secondary", className="me-1")
            ], style={"padding-top": "20px"}),
            html.Div([

            ], id="div-response-store", style={"padding-top": "20px"}),
        ])
])

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


def createTable(df):
    table = html.Div(
        dash_table.DataTable(df.head(10).to_dict('records'), [{"name": i, "id": i} for i in df.columns])
    )
    return table


@app.callback(Output("page-content", "children"), [Input("url", "pathname")],
              Input(component_id='dropdown', component_property="value"))
def render_page_content(pathname, dropdown):

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
                html.H1("Error: Seleccione una acción",
                        className="text-danger"),
                html.Hr(),
                html.P(f"Porfavor seleccione que desea realizar"),
            ],
            className="p-3 bg-light rounded-3",
        )


def analytics_purchasing(pathname):
    if pathname == "/DATOS":
        return createTable(df)
    elif pathname == "/INFERENCIA":
        return inferenciaTarget1
    # If the user tries to reach a different page, return a 404 message
    return getDivError(pathname)


def analytics_profiles(pathname):
    if pathname == "/DATOS":
        return createTable(df)
    elif pathname == "/INFERENCIA":
        return "inferencia perfiles"
    # If the user tries to reach a different page, return a 404 message
    return getDivError(pathname)


def analytics_campaign(pathname):
    if pathname == "/DATOS":
        return createTable(df)
    elif pathname == "/INFERENCIA":
        return "inferencia campaña"
    # If the user tries to reach a different page, return a 404 message
    return getDivError(pathname)


def analytics_expenses(pathname):
    if pathname == "/DATOS":
        return createTable(df)
    elif pathname == "/INFERENCIA":
        return "inferencia gastos"
    # If the user tries to reach a different page, return a 404 message
    return getDivError(pathname)


def getDivError(pathname):
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


@app.callback(Output(component_id="div-response-catalog", component_property="children"),
              Input(component_id='submitCatalog', component_property='n_clicks'),
              Input(component_id="mntWinesCatalog", component_property="value"),
              Input(component_id="mntMeatProductsCatalog", component_property="value"),
              Input(component_id="incomeCatalog", component_property="value"),
              Input(component_id="numStorePurchasesCatalog", component_property="value"),
              Input(component_id="mntGoldProdsCatalog", component_property="value"),
              Input(component_id="mntFruitsCatalog", component_property="value"),
              Input(component_id="mntFishProductsCatalog", component_property="value"),
              Input(component_id="mntSweetProductsCatalog", component_property="value"),
              Input(component_id="numWebPurchasesCatalog", component_property="value"),
              Input(component_id="kidhomeCatalog", component_property="value"),
              Input(component_id="numWebVisitsMonthCatalog", component_property="value"),
              )
def inferencia_catalog(n_clicks, mntWinesCatalog, mntMeatProductsCatalog, incomeCatalog, numStorePurchasesCatalog, mntGoldProdsCatalog, mntFruitsCatalog
, mntFishProductsCatalog, mntSweetProductsCatalog, numWebPurchasesCatalog, kidhomeCatalog, numWebVisitsMonthCatalog):
    if ("submitCatalog" == ctx.triggered_id):
        catalog_model = joblib.load("../persistencia/catalog_model.joblib")

        input = pd.DataFrame()

        input["MntWines"] = [mntWinesCatalog]
        input["MntMeatProducts"] = [mntMeatProductsCatalog]
        input["Income"] = [incomeCatalog]
        input["NumStorePurchases"] = [numStorePurchasesCatalog]
        input["MntGoldProds"] = [mntGoldProdsCatalog]
        input["MntFruits"] = [mntFruitsCatalog]
        input["MntFishProducts"] = [mntFishProductsCatalog]
        input["MntSweetProducts"] = [mntSweetProductsCatalog]
        input["NumWebPurchases"] = [numWebPurchasesCatalog]
        input["Kidhome"] = [kidhomeCatalog]
        input["NumWebVisitsMonth"] = [numWebVisitsMonthCatalog]

        result = catalog_model.predict(input)[0]

        return (f"El cliente que ingreso podria realizar {result} compras al mes")

    

@app.callback(Output(component_id="div-response-web", component_property="children"),
              Input(component_id='submitWeb', component_property='n_clicks'),
              Input(component_id="mntWinesWeb", component_property="value"),
              Input(component_id="mntMeatProductsWeb", component_property="value"),
              Input(component_id="incomeWeb", component_property="value"),
              Input(component_id="numStorePurchasesWeb", component_property="value"),
              Input(component_id="mntGoldProdsWeb", component_property="value"),
              Input(component_id="mntFruitsWeb", component_property="value"),
              Input(component_id="mntFishProductsWeb", component_property="value"),
              Input(component_id="mntSweetProductsWeb", component_property="value"),
              Input(component_id="numCatalogPurchasesWeb", component_property="value"),
              Input(component_id="kidhomeWeb", component_property="value"),
              Input(component_id="numWebVisitsMonthWeb", component_property="value"),
              )
def inferencia_Web(n_clicks, mntWinesWeb, mntMeatProductsWeb, incomeWeb, numStorePurchasesWeb, mntGoldProdsWeb, mntFruitsWeb
, mntFishProductsWeb, mntSweetProductsWeb, numCatalogPurchasesWeb, kidhomeWeb, numWebVisitsMonthWeb):
    if ("submitWeb" == ctx.triggered_id):
        web_model = joblib.load("../persistencia/page_web_model.joblib")

        input = pd.DataFrame()

        input["MntWines"] = [mntWinesWeb]
        input["MntMeatProducts"] = [mntMeatProductsWeb]
        input["Income"] = [incomeWeb]
        input["NumStorePurchases"] = [numStorePurchasesWeb]
        input["MntGoldProds"] = [mntGoldProdsWeb]
        input["MntFruits"] = [mntFruitsWeb]
        input["MntFishProducts"] = [mntFishProductsWeb]
        input["MntSweetProducts"] = [mntSweetProductsWeb]
        input["NumCatalogPurchases"] = [numCatalogPurchasesWeb]
        input["Kidhome"] = [kidhomeWeb]
        input["NumWebVisitsMonth"] = [numWebVisitsMonthWeb]

        result = web_model.predict(input)[0]

        return (f"El cliente que ingreso podria realizar {result} compras al mes")



@app.callback(Output(component_id="div-response-store", component_property="children"),
              Input(component_id='submitStore', component_property='n_clicks'),
              Input(component_id="mntWinesStore", component_property="value"),
              Input(component_id="mntMeatProductsStore", component_property="value"),
              Input(component_id="incomeStore", component_property="value"),
              Input(component_id="numWebPurchasesStore", component_property="value"),
              Input(component_id="mntGoldProdsStore", component_property="value"),
              Input(component_id="mntFruitsStore", component_property="value"),
              Input(component_id="mntFishProductsStore", component_property="value"),
              Input(component_id="mntSweetProductsStore", component_property="value"),
              Input(component_id="numCatalogPurchasesStore", component_property="value"),
              Input(component_id="kidhomeStore", component_property="value"),
              Input(component_id="numWebVisitsMonthStore", component_property="value"))
def inferencia_store(n_clicks, mntWinesStore, mntMeatProductsStore, incomeStore, numWebPurchasesStore, mntGoldProdsStore, mntFruitsStore
, mntFishProductsStore, mntSweetProductsStore, numCatalogPurchasesStore, kidhomeStore, numWebVisitsMonthStore):
    if ("submitStore" == ctx.triggered_id):
        store_model = joblib.load("../persistencia/physical_store_model.joblib")

        input = pd.DataFrame()

        input["MntWines"] = [mntWinesStore]
        input["MntMeatProducts"] = [mntMeatProductsStore]
        input["Income"] = [incomeStore]
        input["NumWebPurchases"] = [numWebPurchasesStore]
        input["MntGoldProds"] = [mntGoldProdsStore]
        input["MntFruits"] = [mntFruitsStore]
        input["MntFishProducts"] = [mntFishProductsStore]
        input["MntSweetProducts"] = [mntSweetProductsStore]
        input["NumCatalogPurchases"] = [numCatalogPurchasesStore]
        input["Kidhome"] = [kidhomeStore]
        input["NumWebVisitsMonth"] = [numWebVisitsMonthStore]

        result = store_model.predict(input)[0]

        return (f"El cliente que ingreso podria realizar {result} compras al mes")


if __name__ == '__main__':
    app.run_server(debug=True)
