import json
from subprocess import call
from dash import html, dash_table, callback, Output, Input, State, dcc
import pandas as pd
from src.static import SQLStatements, ColumnNames
from src.extensions import db
import plotly.express as px
import pycountry
# from utils.sqlcommands import sql_get_rses
# from utils.connectionpool import pool

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

# layout = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])


layout = html.Div([
    dash_table.DataTable(
        id='rucio_rse_list',
        columns=[
            {"name": i, "id": i, 'presentation': 'markdown'} 
            if i == 'rse' 
            else 
            {"name": i, "id": i, } 
            for i in ColumnNames.rse_table
        ],

        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_action="native",
        page_current=0,
        page_size=10,
        markdown_options = {'link_target': "_self"},
        export_format="csv"
    ),
    dcc.Graph(id="rse_graph"),
    dcc.Graph(id="account_usage_graph")
    # html.Pre(id='account_usage_graph', style={
    #     'border': 'thin lightgrey solid',
    #     'overflowX': 'scroll'
    # }),
    # html.Div(id='account_usage_graph')
])


@callback(
    Output('rucio_rse_list', 'data'),
    # Output('graph', 'figure'), #M
    # Input('rucio_rse_list', "page_current"),
    Input('rucio_rse_list', "page_size"),
)
def get_rses_list(_):

    rses = db.session.execute(SQLStatements.get_rses)
    data = rses.fetchall()
    rse_data_pd = pd.DataFrame(data, columns=ColumnNames.rse_table)

    # fig = get_map_data(rse_data_pd) #M

    rse_data_pd['rse_id']=rse_data_pd['rse_id'].apply(lambda x: x.hex())
    
    rse_data_pd.loc[:, 'rse'] = rse_data_pd.rse.apply(lambda rse_name: f'[{rse_name}](/rses/?rse={rse_name})')

    data = rse_data_pd.to_dict('records')
        
    return data



# def get_map_data(df): #M
#     df[['tier', 'country', 'Extra']] = df['rse'].str.split('_', n=2, expand=True)
#     df['country'] = df['country'].apply(lambda x: pycountry.countries.get(alpha_2 = x).alpha_3 if pycountry.countries.get(alpha_2 = x) else 'GBR')

#     df = df[['tier', 'country', 'used']]
#     fig = px.scatter_geo(df, locations="country", color="tier", hover_name="country", size="used", projection="natural earth")
#     return fig


@callback(
    Output('rse_graph', 'figure'),
    Input('rucio_rse_list', 'derived_virtual_data'),
)
def get_rse_usage_graph(data):
    data_df = pd.DataFrame(data, columns=ColumnNames.rse_table)
    data_df.rse = data_df.rse.apply(lambda x: x.split('=')[1][:-1])
    data_df["tier"] = data_df.rse.apply(lambda x: x.split('_')[0])
    # print(data_df.head())
    fig = px.bar(data_df, x='rse', y='used',
            color='tier',
             text_auto='.2s', height=800)
    fig.update_layout(clickmode='event')

    return fig

@callback(
    Output('account_usage_graph', 'figure'),
    Input('rse_graph', 'clickData'),
)
def get_account_usage_graph(clickData):
    if not clickData:
        return "None"
    rse = clickData["points"][0]["x"]
    rse_id = get_rse_id_from_name(rse)
    usage = db.session.execute(SQLStatements.get_usage_by_account.format(rse_id))
    data = usage.fetchall()
    usage_data_pd = pd.DataFrame(data, columns=ColumnNames.usage_graph)
    # print(usage_data_pd.head())
    fig = px.bar(usage_data_pd, x='account', y='sum_bytes',
            color='account', text_auto='.3s',
            )
    return fig


    



def get_rse_id_from_name(rse_name):
    with open('rse_id_from_name.json', 'r') as f:
        rse_id_from_name_map = json.load(f)
    
    return rse_id_from_name_map[rse_name]