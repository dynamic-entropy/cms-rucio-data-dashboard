from dash import dcc, html, dash_table
import pandas as pd
from src.static import ColumnNames
from src.dash_app.dashapp_common import header

def rules_on_did_table(title, id):
    rule_table = html.Div(
        [
            html.H5(title, className='mt-5 border-bottom text-secondary'),
            dash_table.DataTable(
                id=id,
                columns=[
                {"name": i, "id": i, "deletable":False, "selectable": True, 'presentation': 'markdown'} 
                if i == 'id' 
                else 
                {"name": i, "id": i, "deletable":False, "selectable": True} 
                for i in ColumnNames.rules_on_did
                ],
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                page_action="native",
                page_current=0,
                page_size=10,
                markdown_options = {'link_target': "_self"},
                export_format="csv"
            )
        ]
    )
    
    return rule_table

def rules_on_children_table(title, id):
    rule_table = html.Div(
        [
            html.H5(title, className='mt-5 border-bottom text-secondary'),
            dash_table.DataTable(
                id=id,
                columns=[
                {"name": i, "id": i, "deletable":False, "selectable": True, 'presentation': 'markdown'} 
                if i == 'id' 
                else 
                {"name": i, "id": i, "deletable":False, "selectable": True} 
                for i in ColumnNames.rules_on_children
                ],
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                page_action="native",
                page_current=0,
                page_size=10,
                markdown_options = {'link_target': "_self"},
                export_format="csv"
            )
        ]
    )
    
    return rule_table

    
layout = html.Div(
    children=[
        header.layout,
        html.Div(
            className="container",
            style= {'max-width': '95%'},
            children = [
                html.H3("Enter DID to search", className='mt-5 border-bottom rounded'),
                dcc.Input(id="did_input", placeholder='file | dataset | container name', debounce=True, className="form-control"),
                html.Div(id="did_type"),
                html.Div(
                    id="did_replica_info",
                ),
                dcc.Loading(
                    id="loading_did",
                    type="circle",
                    children=html.Div(
                        id="rules_on_did",
                        children=[
                            rules_on_did_table(title, id) for title,id in [   
                                ("Rules on file","rules_on_file"), 
                                ("Rules on dataset", "rules_on_dataset"),
                                ("Rules on container", "rules_on_container")
                            ]
                        ] + [ rules_on_children_table("Rules on DID Children", "rules_on_children")]
                    )
                ),                
            ]
        )
    ],
)





