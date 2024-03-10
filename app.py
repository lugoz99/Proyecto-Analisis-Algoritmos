# app.py
# Importaciones de librerías
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import dash_cytoscape as cyto
import os
import json

#Importaciones de carpetas y funciones
from layouts.navbar import navbar
from layouts.form_page import form_page
from utils.visualization import update_network,update_network_personalizado
from helpers.form import get_form_data
from layouts.general_layouts import upload_component, rename_file
from callbacks.callbacks import register_callbacks

cyto.load_extra_layouts()

# Crear la aplicación de Dash

app = dash.Dash(__name__,prevent_initial_callbacks='initial_duplicate', suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, "style.css"])
register_callbacks(app)
# Crear el diseño de la aplicación

# función para obtener el div del grafo de la red
def get_graph_div(elements, stylesheet=None):
    return html.Div(id='network-graph-container', className="container", children=[
        dcc.Loading(
            id="loading-graph",
            type="circle",
            children=[
                cyto.Cytoscape(
                    id='network-graph',
                    layout={'name': 'random'},
                    style={'width': '100%', 'height': '800px'},
                    stylesheet=stylesheet,
                    elements=elements,
                    generateImage={'type': 'png', 'action': 'store'},
                    imageData=None
                ),
            ]
        ),
    ])




app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='form-data-store'),
    dcc.Store(id='network-elements'),
    dcc.Store(id='network-stylesheet'),
    dcc.Store(id='random-clicks', data=0),
    dcc.Store(id='image-data-store'),
    dcc.Store(id='network-graph-elements', data=None),
    #get_graph_div([], stylesheet=None) , # Asegúrate de que get_graph_div está definido antes de usarlo aquí
    navbar,
    html.Div(id='page-content'),

    
])
# Callbacks para manejar la navegación y el almacenamiento de datos del formulario


# Callback para mostrar la página correspondiente
@app.callback(
    Output('page-content', 'children',allow_duplicate=True),
    [Input('form-data-store', 'data'),
    Input('url', 'pathname'),
    Input('random-clicks', 'data')],
    [State('image-data-store', 'data')],
   # Input('network-graph-elements', 'data'),
    prevent_initial_call=True
)
def display_page(form_data,pathname,n_clicks,imageData):
    if pathname == '/grafica':
        if imageData is not None:
            dcc.Store(id='image-data-store', data=imageData)
            img = html.Img(src=imageData)
            return html.Div(img)
        else:
            return "No hay imagen para mostrar"
    if pathname == '/formulario':
        return form_page
    if pathname == '/aleatorio':
            elements, stylesheet = update_network()
            return get_graph_div(elements, stylesheet)
    if pathname == '/personalizado':
            # Aquí puedes utilizar los datos del formulario para personalizar la página
            elements, stylesheet = grafo_personalizado(form_data)
            return get_graph_div(elements, stylesheet)
    if pathname == '/cargar-json':
        # TODO: Agregar la página para cargar un archivo JSON
            return upload_component
    if pathname == '/guardar-como':
         return rename_file
  
    else:
        return "Esta es la página de inicio"  # Puedes reemplazar esto con tu propia página de inicio



def grafo_personalizado(form_data):
    n_nodes, is_complete, is_connected, is_weighted, is_directed = get_form_data(form_data)
    if n_nodes is not None:
        return update_network_personalizado(n_nodes, is_weighted, is_directed, is_connected, is_complete)
    return None, None




@app.callback(
    Output('random-clicks', 'data'),
    [Input('generate-random', 'n_clicks')]
)
def update_random_clicks(n_clicks):
    return n_clicks



if __name__ == '__main__':
    app.run_server(debug=True)

