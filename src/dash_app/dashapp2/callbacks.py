from ntpath import join
import time
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
import pandas as pd
from src.extensions import db
from src.static import ColumnNames, SQLStatements
from dash import dash_table, html

def register_callbacks(dashapp):
    @dashapp.callback(
        Output("rules_on_file", "data"), 
        Output("rules_on_dataset", "data"),
        Output("rules_on_container", "data"),
        Output("rules_on_children", "data"),
        Output("did_replica_info", "children"),
        Output("did_type", "children"),
        Output("did_type", 'className'),
        Input("did_input", "value")
    )
    def rules_on_did_family(did):
        rules_data = {"file": [], "dataset":[], "container": [], "children": []}
        did_replica_info = ""
        class_name, children = "", ""

        if did:
            class_name = 'badge bg-danger'
            children = html.Div(["DID Not Found:  ", html.B(did)])
            did_type = get_did_type(did)
            original_flag = True
            if did_type:
                class_name = 'badge bg-success'
                children = f"DID Type: {did_type}"

                if did_type == 'F':
                    did_replica_info = get_did_replica_info_table(did, did_type)
        
                    rules_data["file"] = get_rules_for_did(did)
                    did = get_parent_did(did)
                    did_type='D'
                    original_flag = False
                
                if did and did_type == 'D':
                    if original_flag:
                        did_replica_info = get_did_replica_info_table(did, did_type)
                        rules_data["children"] += get_rules_for_did(did, bulk=True)

                    rules_data["dataset"] = get_rules_for_did(did)
                    did = get_parent_did(did)
                    did_type='C'
                    original_flag = False
                
                if did and did_type == 'C':
                    if original_flag:
                        rules_data["children"] += get_rules_for_did(did, bulk=True)

                    while did:
                        rules_data["container"] += get_rules_for_did(did)
                        did = get_parent_did(did)


        for key in rules_data:
            if not rules_data[key]:
                rules_data[key] = pd.DataFrame([], columns=ColumnNames.rules_on_did).to_dict('records')
        

        return rules_data["file"], rules_data["dataset"], rules_data["container"], rules_data["children"], did_replica_info, children, class_name


def get_rules_for_did(did, bulk=False):

    if bulk:
        child_dids = get_child_dids(did)
        child_dids = [f"('{child_did[0]}', {0})" for child_did in child_dids]
        child_dids_string = ", ".join(child_dids)
        rules = db.session.execute(SQLStatements.get_rules_for_did_bulk.format(child_dids_string))
    else:
        rules = db.session.execute(SQLStatements.get_rules_for_did.format(did))

    rules_data = rules.fetchall()
    rules_data_pd = pd.DataFrame(rules_data, columns=ColumnNames.rules_on_did)

    rules_data_pd['id'] = rules_data_pd['id'].apply(lambda x: x.hex())
    rules_data_pd.loc[:, 'id'] = rules_data_pd.id.apply(lambda rule_id: f'[{rule_id}](https://cms-rucio-webui.cern.ch/rule?rule_id={rule_id})')

    data = rules_data_pd.to_dict('records')

    return data


def get_parent_did(did):
    did = db.session.execute(SQLStatements.get_parent_did.format(did)).fetchall()
    if did:
        did = did[0][0]
    return did

def get_child_dids(did):
    dids = db.session.execute(SQLStatements.get_child_did.format(did)).fetchall()
    return dids

def get_did_replica_info_table(did, did_type):
    if did_type == 'F':
        file_replica_info = db.session.execute(SQLStatements.get_file_replica_info.format(did)).fetchall()
        return dash_table.DataTable(
                        data = pd.DataFrame(file_replica_info, columns=ColumnNames.file_replica_info).to_dict('records'),
                        columns = [{"name": i, "id": i} for i in ColumnNames.file_replica_info]
                    ) 
    dataset_replica_info = db.session.execute(SQLStatements.get_dataset_replica_info.format(did)).fetchall()
    return dash_table.DataTable(
                    data = pd.DataFrame(dataset_replica_info, columns=ColumnNames.dataset_replica_info).to_dict('records'),
                    columns = [{"name": i, "id": i} for i in ColumnNames.dataset_replica_info]
                ) 
                

def get_did_type(did):
    did_type = db.session.execute(SQLStatements.get_did_type.format(did)).fetchone()
    if did_type:
        did_type = did_type[0]
    return did_type

