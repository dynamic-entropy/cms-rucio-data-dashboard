from importlib.resources import path
from dash.dependencies import Input
from dash.dependencies import Output
from dash import html
from src.extensions import db
from src.dash_app.dashapp1.pages import containers_page, rses_page, datasets_page, rules_page
from src.dash_app.dashapp_common import header
import re

def register_callbacks(dashapp):
    @dashapp.callback(
    Output('page-header', 'children'),
    Output('page-content', 'children'),
    Input('url', 'search')
    )
    def load_pages(search):

        content_page = html.Div()
        if re.match(r"\?rse=.+", search):
            content_page = datasets_page
        elif re.match(r"\?container=.+", search):
            content_page = datasets_page
        elif re.match(r"\?dataset=.+", search):
            content_page = rules_page
        else:
            content_page = rses_page

        return header.layout, content_page.layout