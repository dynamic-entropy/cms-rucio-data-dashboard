from flask import Flask
from dash import Dash
from config import BaseConfig
from dash import html
from flask.helpers import get_root_path

def init_app():
    """Construct core flask application"""

    server = Flask(__name__, instance_relative_config=False)
    server.config.from_object(BaseConfig)
    # server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    register_dashapps(server)
    register_extensions(server)
    register_blueprints(server)

    return server
    


def register_dashapps(app):
    from src.dash_app.dashapp1 import layout as layout1
    from src.dash_app.dashapp1 import callbacks as callbacks1
    from src.dash_app.dashapp1.pages import containers_page, rses_page, datasets_page, rules_page


    from src.dash_app.dashapp2 import layout as layout2
    from src.dash_app.dashapp2 import callbacks as callbacks2

    from src.dash_app.dashapp_common import header

    register_dash_app(app, 'Dashapp 1', layout1, [containers_page, rses_page, header, datasets_page, rules_page, layout1], '/rses/', callbacks1)
    register_dash_app(app, 'Dashapp 2', layout2, [layout2], '/did-rule-info/', callbacks2)

def register_extensions(server):
    from src.extensions import db
    db.init_app(server)


def register_blueprints(server):
    from src.routes import server_bp
    server.register_blueprint(server_bp)

def register_dash_app(app, title, layout, validation_layouts, url_base_path, callbacks_func):
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no"
    }

    dashapp = Dash(__name__,
                    server=app,
                    url_base_pathname=url_base_path,
                    assets_folder=get_root_path(__name__) + '/dash_app/assets/',
                    meta_tags=[meta_viewport],
                    # external_scripts=[
                    #     {
                    #         "src":"https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js",
                    #         "integrity":"sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p",
                    #         "crossorigin":"anonymous"
                    #     },
                    # ],
                )

    with app.app_context():
        from src.dash_app.dashapp1.pages import containers_page, rses_page, datasets_page, rules_page
        dashapp.title = title
        dashapp.layout = layout.layout
        dashapp.validation_layout = html.Div([l.layout for l in validation_layouts])
        callbacks_func.register_callbacks(dashapp) 
