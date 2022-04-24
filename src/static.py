from re import match

class SQLStatements:
    get_rses = "select rse_usage.rse_id, rses.rse, rse_usage.used, rse_usage.files, rse_usage.updated_at, rse_usage.created_at from cms_rucio_prod.rse_usage join cms_rucio_prod.rses on rses.id = rse_usage.rse_id and rse_usage.source='rucio' and rses.rse_type='DISK' and rses.rse not like '%Test' and rses.rse not like '%Temp'"
    get_datasets = "select NAME ,BYTES ,LENGTH ,AVAILABLE_REPLICAS_CNT ,UPDATED_AT ,CREATED_AT  from cms_rucio_prod.collection_replicas where rse_id='{0}' and state='A' order by {1} {2} offset {3} rows fetch next {4} rows only"
    get_datasets_with_filter = "select NAME ,BYTES ,LENGTH ,AVAILABLE_REPLICAS_CNT ,UPDATED_AT ,CREATED_AT  from cms_rucio_prod.collection_replicas where rse_id='{0}' and state='A' and {1} like '%{2}%' order by {3} {4} offset {5} rows fetch next {6} rows only"
    get_rules = "select ID ,ACCOUNT ,NAME ,DID_TYPE ,STATE ,RSE_EXPRESSION ,COPIES ,LOCKED ,ACTIVITY ,GROUPING ,NOTIFICATION ,PRIORITY ,META ,UPDATED_AT ,CREATED_AT  from cms_rucio_prod.rules where name='{0}'"
    get_did_type = "select did_type from CMS_RUCIO_PROD.dids where name='{0}'"
    get_rules_for_did = "select id, account, rse_expression, activity, created_at, updated_at from cms_rucio_prod.rules where name='{0}'"
    get_parent_did = "select name from cms_rucio_prod.contents where child_name='{0}'"
    get_file_replica_info = "select rse.rse, rep.updated_at, rep.created_at from cms_rucio_prod.replicas rep join cms_rucio_prod.rses rse on rep.rse_id = rse.id and rep.name='{0}'"
    get_dataset_replica_info = "select rse.rse, rep.available_replicas_cnt, rep.updated_at, rep.created_at from cms_rucio_prod.collection_replicas rep join cms_rucio_prod.rses rse on rep.rse_id = rse.id and rep.name='{0}'"

    def get_datasets_query(rse_id=None, filter_query=None, sort_by=None, paginate=None):
        query = "select NAME ,BYTES ,LENGTH ,AVAILABLE_REPLICAS_CNT ,UPDATED_AT ,CREATED_AT from cms_rucio_prod.collection_replicas"

        if rse_id:
            query += f" where rse_id='{rse_id}' and state='A'"
        
        if rse_id and filter_query:
            m = match(r"{(.+)} s.+ (.+)", filter_query)
            column_name, filter_string = m.group(1), m.group(2)
            query += f" and {column_name} like '%{filter_string}%'"
        
        if sort_by:
            column_id, direction = sort_by[0]['column_id'], sort_by[0]['direction']
            query += f" order by {column_id} {direction}"

        if paginate:
            offset, psize = paginate["offset"], paginate["psize"]
            query += f" offset {offset} rows fetch next {psize} rows only"

        return query


class ColumnNames:
    rse_table = ['rse_id', 'rse', 'used', 'files', 'updated_at', 'created_at']
    dataset_table = ['name', 'bytes', 'length', 'available_replicas_cnt', 'updated_at', 'created_at']
    rules_table = ['id', 'account', 'name', 'did_type', 'state', 'rse_expression', 'copies', 'locked', 'activity', 'grouping', 'notification', 'priority', 'meta', 'updated_at', 'created_at']
    rules_on_did = ['id', 'account', 'rse_expression', 'activity', 'created_at', 'updated_at' ]
    file_replica_info = ['rse', 'updated_at', 'created_at']
    dataset_replica_info = ['rse', 'available_replicas_cnt', 'updated_at', 'created_at']