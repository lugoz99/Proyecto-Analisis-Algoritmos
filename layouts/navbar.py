import dash_bootstrap_components as dbc
from dash import html, dcc

header = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Grafo", header=True),
                dbc.Button("Aleatorio", 
                           id="generate-button",
                           className="dropdown-item ",
                           n_clicks=0,
                           ),
            ],
            nav=True,
            in_navbar=True,
            label="Generar",
        ),
        
         dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Grafo", header=True),
                dbc.Button("Proceso 1", 
                           id="generate-button-procees-1",
                           className="dropdown-item ",
                           n_clicks=0,
                           ),
            ],
            nav=True,
            in_navbar=True,
            label="Procesos",
        ),

        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Archivos", header=True),
                dcc.Upload(
                    id='open-file',
                    children=html.Button('Abrir Archivo', className='btn btn-primary', style={'margin': '10px'}),
                    style={
                        'display': 'inline-block'
                    }
            ),
                
                dbc.DropdownMenuItem(dbc.Button("Cerrar", id='close-file', className="dropdown-item")),
                dbc.DropdownMenuItem(html.Button("Guardar", id="btn-download-txt", className="dropdown-item")),
                dbc.DropdownMenuItem(dcc.Download(id="download-text")),
                dbc.DropdownMenuItem(dbc.Button("Guardar Como", id='save-file-as', className="dropdown-item")),
            ],
            nav=True,
            in_navbar=True,
            label="Operaciones archivos",
        ),


        dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Importar Datos", header=True),
                    dbc.DropdownMenuItem("Formato txt", href="#"),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Exportar datos", header=True),
                    dbc.DropdownMenuItem(
                        html.Div(
                            children=[
                                dcc.Download(id="download-excel"),
                                html.Button("En Excel", id="btn", n_clicks=0, className="btn btn-primary"),
                            ],
                        ),
                    ),
                    dbc.DropdownMenu(
                        label="Imagen",
                        size="md",
                        className="mb-3 mx-3",
                        children=[
                            dbc.DropdownMenuItem(
                                html.Div(
                                    dbc.Button("PNG", color="primary", className="mx-auto d-flex w-100", id="btn-get-png"),
                                    className="d-flex"
                                ),
                        ),
                            dbc.DropdownMenuItem(
                                html.Div(
                                    dbc.Button("JPG", color="secondary", className="mx-auto d-flex w-100",id="btn-get-jpg"),
                                    className="d-flex"
                                ),
                            ),
                        ],
                    )
                ],
                nav=True,
                in_navbar=True,
                label="Gestion datos",
            ),
               dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Ver Modo", header=True),
                    #dbc.DropdownMenuItem("Grafica", id='id-grafica',href="/grafica"),
                    dbc.Button("Grafica", id='id-grafica', href="/grafica", className="m-2"),
                    dbc.Button("Tabla", id='id-table', href="/tabla",className="m-2"),

                ],
                nav=True,
                in_navbar=True,
                label="Ventana",
            ),

    ],
    brand="Proyecto Análisis y Diseño de Algoritmos - 2024",
    brand_href="/",
    color= '#1f618d ',
    sticky="top",
    dark=True,
)