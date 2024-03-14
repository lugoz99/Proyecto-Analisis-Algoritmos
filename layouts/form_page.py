# layouts/form_page.py

import dash_bootstrap_components as dbc
from dash import html

form_page = html.Div(className="card container mt-2 d-flex", children=[
    html.H2("Personaliza tu grafo"),
    dbc.CardGroup(
        [
            dbc.Label("Número de nodos"),
            dbc.Input(type="number", id="n-nodes-input", min=1,value=False),
        ]
    ),
    dbc.CardGroup(
        [
            dbc.Label("¿Es completo?", style={"margin-right": "22px"}),
            dbc.Checkbox(id="is-complete-input",value=False),
        ]
        ,className="mt-2"

    ),
    dbc.CardGroup(
        [
            dbc.Label("¿Es conexo?", style={"margin-right": "38px"}),
            dbc.Checkbox(id="is-connected-input",value=False),
        ]
    ),
    dbc.CardGroup(
        [
            dbc.Label("¿Es ponderado?", style={"margin-right": "10px"}),
            dbc.Checkbox(id="is-weighted-input",value=False),
        ]
    ),
    dbc.CardGroup(
        [
            dbc.Label("¿Es dirigido?", style={"margin-right": "33px"}),
            dbc.Checkbox(id="is-directed-input", value=False),
        ]
    ),
])


modal = dbc.Modal(
    [
        dbc.ModalHeader("Formulario"),
        dbc.ModalBody(
            form_page
        ),
        dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ms-auto", n_clicks=0
                    )
                ),
    ],
    id="modal",
    is_open=False,
)