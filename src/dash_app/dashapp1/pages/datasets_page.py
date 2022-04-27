from dash import html, dash_table, Input, Output, State, callback, dcc
import re
import json
import pandas as pd
from urllib.parse import quote
from src.static import SQLStatements, ColumnNames
from src.extensions import db


layout = dcc.Loading(
    children= [
        dash_table.DataTable(
            id='rucio_datasets_list',
            columns=[
                {"name": i, "id": i, 'presentation': 'markdown'} 
                if i == 'name' 
                else 
                {"name": i, "id": i,} 
                for i in ColumnNames.dataset_table
            ],
            filter_action="custom",
            filter_query="",
            sort_action="custom",
            sort_mode="single",
            page_action="custom",
            page_current=0,
            page_size=10,
            export_format="csv",
            markdown_options = {'link_target': "_self"},
            style_data = {
            'whiteSpace': 'normal',
            'height': 'auto',
            'backgroundColor': 'white'
            },
            style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{state} = "U"'
                    },
                    'backgroundColor': '#FFF4F4',
                }
            ],
            style_header={
                'color': 'black',
                'fontWeight': 'bold',
                'text-transform': 'uppercase'
            }

        ),  
    ],
    id='loading_rucio_datasets_list'
)
 

def get_rse_id_from_name(rse_name):
    with open('rse_id_from_name.json', 'r') as f:
        rse_id_from_name_map = json.load(f)
    
    return rse_id_from_name_map[rse_name]

@callback(
    Output('rucio_datasets_list', 'data'),
    Input('rucio_datasets_list', "page_current"),
    Input('rucio_datasets_list', "page_size"),
    Input('rucio_datasets_list', 'sort_by'),
    Input('rucio_datasets_list', 'filter_query'),
    State('url', 'search')
)
def get_datasets_list(page_current, page_size, sort_by, filter_query, search):
    m = re.match(r"\?rse=(.+)", search)
    rse_name = m.group(1)
    rse_id = get_rse_id_from_name(rse_name)

    paginate = {
        "offset": page_current * page_size,
        "psize": page_size
    }

    print("rse_id", rse_id)
    print("filter_query", filter_query)
    print("sort_by", sort_by)
    print("paginate", paginate)

    query = SQLStatements.get_datasets_query(rse_id, filter_query, sort_by, paginate)
    print('query = ', query)
    datasets = db.session.execute(query)
        
    data = datasets.fetchall()
    dataset_data_pd = pd.DataFrame(data, columns=ColumnNames.dataset_table)
    dataset_data_pd.loc[:, 'name'] = dataset_data_pd.name.apply(lambda dataset_name: f'[{dataset_name}](/rses/?dataset={quote(dataset_name)})')
    data = dataset_data_pd.to_dict('records')
    return data
