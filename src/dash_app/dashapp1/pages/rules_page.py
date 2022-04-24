from email.quoprimime import unquote
from dash import html, dash_table, callback, Input, Output, State
import pandas as pd
import re
from urllib.parse import unquote

from src.static import SQLStatements, ColumnNames
from src.extensions import db

layout = dash_table.DataTable(
    id='rucio_rules_list',
    columns=[
        {"name": i, "id": i, 'presentation': 'markdown'} 
        if i == 'id' 
        else 
        {"name": i, "id": i,} 
        for i in ColumnNames.rules_table
    ],
    # data = rules_df.to_dict('records'),
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    column_selectable="single",
    row_selectable="multi",
    selected_columns=[],
    selected_rows=[],
    page_action="native",
    page_current=0,
    page_size=10,
)

@callback(
    Output('rucio_rules_list', 'data'),
    # Input('rucio_rules_list', "page_current"),
    Input('rucio_rules_list', "page_size"),
    State('url', 'search')
)
def get_rules_list(_, search):
    m = re.match(r"\?dataset=(.+)", search)
    # m = re.match(r"/rse/(.+?)/(.+)", pathname)
    dataset_name = unquote(m.group(1))

    rules = db.session.execute(SQLStatements.get_rules.format(dataset_name))
    data = rules.fetchall()
    rules_data_pd = pd.DataFrame(data, columns=ColumnNames.rules_table)

    rules_data_pd['id'] = rules_data_pd['id'].apply(lambda x: x.hex())
    # rules_data_pd.loc[:, 'name'] = rules_data_pd.name.apply(lambda dataset_name: f'[{dataset_name}](/rses/?dataset={dataset_name})')
    rules_data_pd.loc[:, 'id'] = rules_data_pd.id.apply(lambda rule_id: f'[{rule_id}](https://cms-rucio-webui.cern.ch/rule?rule_id={rule_id})')
    data = rules_data_pd.to_dict('records')
    return data

# def get_did_rules(pathname):
#     m = re.match(r"/rule/(.+)", pathname)
#     did = unquote(m.group(1))
#     client = Client()
#     rules = list(client.list_did_rules(scope='cms', name=did))
#     if len(rules) == 0:
#         rules_df = pd.DataFrame(columns=['id', 'account', 'rse_expression', 'activity', 'created_at', 'updated_at' ])
#     else:
#         rules_df = pd.DataFrame(rules)
#         rules_df = rules_df[['id', 'account', 'rse_expression', 'activity', 'created_at', 'updated_at' ]]
#         rules_df.loc[:, 'id'] = rules_df.id.apply(lambda rule_id: f'[{rule_id}](https://cms-rucio-webui.cern.ch/rule?rule_id={rule_id})')
#     return rules_df