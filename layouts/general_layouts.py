from dash import html,dcc
import dash_bootstrap_components as dbc


upload_component = html.Div([
    dcc.Upload(
        id='upload-json',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    )
])


modal = dbc.Modal(
    [
        dbc.ModalHeader("Formulario"),
        dbc.ModalBody(
            upload_component
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




rename_file = html.Div([

    html.Div(
        style={"margin": "auto","margin-top":"3px", "width": "50%", "padding": "10px" , "text-align": "center", "border": "1px solid black"},
        children = [
            html.H3("Guardar como"),
            dcc.Download(id="download"),
            html.Div(
                style={'display': 'flex', 'justifyContent': 'center'},
                children=[
                    dcc.Input(
                        id="input", 
                        type="text", 
                        required=True,
                        placeholder="Renombrar archivo grafo.json",
                        className="p-1 mt-2",
                        style={'flex': '1', 'marginRight': '10px'}
                    )
                   ]
             ) 
        ])     
])




modal_guardar_como = dbc.Modal(
    [
        dbc.ModalHeader("Formulario"),
        dbc.ModalBody(
            rename_file
        ),
        dbc.ModalFooter(
                    dbc.Button(
                        "Guardar", id="guardar-como", className="ms-auto", n_clicks=0
                    )
                ),
    ],
    id="modal-guardar-como",
    is_open=False,
)

