def get_form_data(form_data):
    if form_data:
        return (
            form_data.get('n_nodes'),
            form_data.get('is_complete'),
            form_data.get('is_connected'),
            form_data.get('is_weighted'),
            form_data.get('is_directed')
        )
    return None, None, None, None, None

