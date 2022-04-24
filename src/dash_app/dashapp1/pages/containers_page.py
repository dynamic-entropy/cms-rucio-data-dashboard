import pickle
from dash import html, dash_table, Input, Output, State, callback
import re
import pandas as pd

# def get_layout(pathname, pool):
#     rse_name = get_rse_name(pathname)
#     _, container_list = get_containers_list(rse_name)

layout = html.Div([
dash_table.DataTable(
    id='container_list',
    # columns=[
    #     {"name": i, "id": i, "deletable":False, "selectable": True, 'presentation': 'markdown'} 
    #     if i == 'container' 
    #     else 
    #     {"name": i, "id": i, "deletable":False, "selectable": True} 
    #     for i in container_list.columns
    # ],
    # data = container_list.to_dict('records'),
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    # column_selectable="single",
    # row_selectable="multi",
    # selected_columns=[],
    # selected_rows=[],
    page_action="native",
    page_current=0,
    page_size=10,
    markdown_options = {'link_target': "_self"}
)   
])


def get_rse_name(pathname):
    m = re.search(r"/rse/(.+)", pathname)
    rse_name = m.group(1)
    return rse_name

@callback(
    Output('container_list', 'data'),
    Input('container_list', "page_current"),
    Input('container_list', "page_size"),
    State('url', 'search'),
)
def get_containers_list(page_current, page_size, rse_name):
    df = get_dataset_data(rse_name)
    df.drop(df[df.bytes==0].index, inplace=True) #removing empty containers and datasets - 0 size
    df.insert(1, "container", [dataset_name[:dataset_name.index("#")] for dataset_name in df['name']])
    container_groups = df.groupby('container', as_index=False)
    container_list = container_groups.agg({'bytes':'sum', 'length':'sum', 'name':'count'})
    container_list.rename(columns={'name':'dataset count'}, inplace=True)
    container_list.loc[:, 'container'] = container_list['container'].apply(lambda cname: f'[{cname}](/rse/{rse_name}/{cname})')
    return container_groups, container_list  


def get_dataset_data(rse_name):
    with open(f'rse_data/{rse_name}.pickle', 'rb') as f:
        rse_data = pickle.load(f)
    rse_data_df = pd.DataFrame(rse_data)
    rse_data_df.drop(rse_data_df[rse_data_df.state == 'UNAVAILABLE'].index, inplace=True)
    return rse_data_df




