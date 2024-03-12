 #TODO: Esto es una configuracion inicial de los nodos y aristas
style_node = {
    "selector":"node",
    'style': {
                'content': 'data(id)',
                'text-valign': 'center',
                'color': 'black',
                'background-color': '#5dade2',
                'shadow-color': 'black',  # Color de la sombra
                'shadow-blur': '10px',  # Tamaño de la sombra
                'shadow-opacity': '0.5'
            }
}

style_edge = {
    "selector":"edge",
    'style': 
            {
                'content': 'data(weight)',
                'line-color': 'black',
                'curve-style': 'bezier',
                'line-style': 'solid',
                'color':' #FF0000',
            }
}