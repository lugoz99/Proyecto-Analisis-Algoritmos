from dash import html,dcc


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
    ),
])


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
                        placeholder="Renombrar archivo",
                        className="p-2 mt-2",
                        style={'flex': '1', 'marginRight': '10px'}
                    ),
                html.Button(
                    "Descargar datos", 
                    id="btn", 
                    n_clicks=0,
                    className="btn btn-primary me-1 p-1",
                    style={'flex': '1','borderRadius': '15px'}
                )
            ]
        ) 
        ])     
])