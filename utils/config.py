config_stylesheet = [
    {
        "selector": "node",
        'style': {
            'content': 'data(label)',
            'text-valign': 'center',
            'color': 'black',
            'background-color': '#5dade2',
            'shadow-color': 'black',  # Color de la sombra
            'shadow-blur': '10px',  # Tamaño de la sombra
            'shadow-opacity': '0.5'
        }
    },
    {
        "selector": "node:selected",
        'style': {
            'background-color': '#FF4136',  # Color de fondo para los nodos cuando están seleccionados
        }
    },
    {
        "selector": "edge",
        'style': {
            'content': 'data(weight)',
            'line-color': 'black',
            'curve-style': 'bezier',
            'line-style': 'solid',
            'color': '#FF0000',
        }
    },
    {
        "selector": "edge:selected",
        'style': {
            'line-color': '#2ECC40',  # Color de línea para las aristas cuando están seleccionadas
        }
    }
]

