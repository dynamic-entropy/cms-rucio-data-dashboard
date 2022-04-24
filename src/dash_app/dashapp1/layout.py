from dash import html, dcc  


layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-header'),
    html.Div(id='page-content', className='container', style= {'max-width': '95%'})
])