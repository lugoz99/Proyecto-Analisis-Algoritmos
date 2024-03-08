# layouts/form_page.py

import dash_bootstrap_components as dbc
from dash import html

form_page = html.Div(className="card container mt-2",children=[


    html.H2("Personaliza tu grafo"),

    dbc.CardGroup(
        [
            dbc.Label("Número de nodos"),
            dbc.Input(type="number", id="n-nodes-input", min=1,value=False),
        ]
    ),
    dbc.CardGroup(
        [
            dbc.Label("¿Es completo?"),
            dbc.Checkbox(id="is-complete-input",value=False),
        ]
    ),
    dbc.CardGroup(
        [
            dbc.Label("¿Es conexo?"),
            dbc.Checkbox(id="is-connected-input",value=False),
        ]
    ),
    dbc.CardGroup(
        [
            dbc.Label("¿Es ponderado?"),
            dbc.Checkbox(id="is-weighted-input",value=False),
        ]
    ),
    dbc.CardGroup(
        [
            dbc.Label("¿Es dirigido?"),
            dbc.Checkbox(id="is-directed-input", value=False),
        ]
    ),
    dbc.Button("Aceptar", id="aceptar", color="primary", href="/personalizado"),
    dbc.Button("Back", id="back", color="primary", href="/"),

])
