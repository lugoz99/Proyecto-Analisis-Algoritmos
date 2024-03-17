from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq


buttons_nodes = dbc.Card(
    [
        dbc.CardHeader("Edición de Nodos"),
        dbc.CardBody(
            [
                dbc.ButtonGroup(
                    [
                        dbc.Button(
                            children=[
                                html.I(
                                    className="bi bi-plus-circle-fill"
                                ),  # Icono de +
                            ],
                            id="add-node-button",
                            color="primary",  # Color del botón
                            className="mr-1",  # Espacio a la derecha del botón
                        ),
                        dbc.Button(
                            children=[
                                html.I(className="bi bi-pencil-fill"),  # Icono de +
                            ],
                            id="update-button",
                            color="secondary",  # Color del botón
                            className="mr-1",  # Espacio a la derecha del botón
                        ),
                        dbc.Button(
                            children=[
                                html.I(className="bi bi-trash3-fill"),  # Icono de +
                            ],
                            id="delete-button",
                            color="danger",  # Color del botón
                            className="mr-1",  # Espacio a la derecha del botón
                        ),
                    ],
                    className="mb-3",  # Margen inferior para separar el grupo de botones del input
                ),
                html.Div(
                    [
                        dcc.Input(
                            id="node-label-input",
                            type="text",
                            placeholder="Etiqueta",
                        ),
                        dcc.Input(
                            id="node-value-input",
                            type="text",
                            placeholder="Valor",
                        ),
                        html.Div(
                            daq.ColorPicker(
                                id="color-picker-node",
                                label="Color",
                                size=150,
                                style={"heigh": "50px"},
                            ),
                            style={"height": "70px", "overflow": "auto"},
                        ),
                    ]
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
            },
        ),
    ],
    style={"width": "18rem"},
)


buttons_edges = dbc.Card(
    [
        dbc.CardHeader("Edición de Aristas"),
        dbc.CardBody(
            [
                dbc.ButtonGroup(
                    [
                        dbc.Button(
                            children=[
                                html.I(
                                    className="bi bi-plus-circle-fill"
                                ),  # Icono de +
                            ],
                            id="add-edge-button",
                            color="primary",  # Color del botón
                            className="mr-1",  # Espacio a la derecha del botón
                        ),
                        dbc.Button(
                            children=[
                                html.I(className="bi bi-pencil-fill"),  # Icono de +
                            ],
                            id="update-edge-button",
                            color="secondary",  # Color del botón
                            className="mr-1",  # Espacio a la derecha del botón
                        ),
                        dbc.Button(
                            children=[
                                html.I(className="bi bi-trash3-fill"),  # Icono de +
                            ],
                            id="delete-edge-button",
                            color="danger",  # Color del botón
                            className="mr-1",  # Espacio a la derecha del botón
                        ),
                    ],
                    className="mb-3",  # Margen inferior para separar el grupo de botones del input
                ),
                html.Div(
                    [
                        dcc.Input(
                            id="edge-label-input",
                            type="text",
                            placeholder="Peso",
                        ),
                        dcc.Dropdown(
                            id="line-style-dropdown",
                            options=[
                                {"label": "Solid", "value": "solid"},
                                {"label": "Dashed", "value": "dashed"},
                            ],
                            value="solid",
                            clearable=False,
                        ),
                        dcc.Checklist(
                            id="arrow-checklist",
                            options=[{"label": "Show Arrow", "value": "show-arrow"}],
                            value=["show-arrow"],
                        ),
                        html.Div(
                            daq.ColorPicker(
                                id="color-picker",
                                label="Color",
                                size=150,
                                style={"heigh": "30px"},

                            ),
                            style={"height": "70px", "overflow": "auto"},
                        ),
                    ]
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
            },
        ),
    ],
    style={"width": "18rem"},
)


contenedor_info = html.Div(
    id="info-grafo",
    style={"background-color":  "#34495e","font-family": "Arial"},
    className="container p-3 rounded-0 shadow-sm text-white",
    children=[
        html.H3("Información de la red"),
    ],
)
