from dash import html, dcc
import dash_bootstrap_components as dbc

buttons_nodes = dbc.Card(
    [
        dbc.CardHeader("Edición de Nodos"),
        dbc.CardBody(
            [
                dbc.ButtonGroup(
                    [
                        dbc.Button(
                            children=[
                                html.I(className="bi bi-plus-circle-fill"),  # Icono de +
                            ],
                            id='add-node-button',
                            color="primary",  # Color del botón
                            className="mr-1"  # Espacio a la derecha del botón
                        ),

                        dbc.Button(
                            children=[
                                html.I(className="bi bi-pencil-fill"),  # Icono de +
                            ],
                            id='update-button',
                            color="secondary",  # Color del botón
                            className="mr-1"  # Espacio a la derecha del botón
                        ),

                        dbc.Button(
                            children=[
                                html.I(className="bi bi-trash3-fill"),  # Icono de +
                            ],
                            id='delete-button',
                            color="danger",  # Color del botón
                            className="mr-1"  # Espacio a la derecha del botón
                        ),
                    ],
                    className="mb-3",  # Margen inferior para separar el grupo de botones del input
                ),
                html.Div([
                    dcc.Input(id="node-label-input", type="text", placeholder="Nodo Seleccionado",
                              style={'marginRight': '10px'}),
                ]),
            ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}
        ),
    ], style={'width': '18rem'}
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
                                html.I(className="bi bi-plus-circle-fill"),  # Icono de +
                            ],
                            id='add-edge-button',
                            color="primary",  # Color del botón
                            className="mr-1"  # Espacio a la derecha del botón
                        ),

                        dbc.Button(
                            children=[
                                html.I(className="bi bi-pencil-fill"),  # Icono de +
                            ],
                            id='update-edge-button',
                            color="secondary",  # Color del botón
                            className="mr-1"  # Espacio a la derecha del botón
                        ),

                        dbc.Button(
                            children=[
                                html.I(className="bi bi-trash3-fill"),  # Icono de +
                            ],
                            id='delete-edge-button',
                            color="danger",  # Color del botón
                            className="mr-1"  # Espacio a la derecha del botón
                        ),
                    ],
                    className="mb-3",  # Margen inferior para separar el grupo de botones del input
                ),
                html.Div([
                    dcc.Input(id="edge-label-input", type="text", placeholder="Arista Seleccionada",
                              style={'marginRight': '10px'}),
                ]),
            ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}
        ),
    ], style={'width': '18rem'}
)