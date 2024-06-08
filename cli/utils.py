
from decimal import Decimal
from money_tracker.daos.sql_generic.factory import SQLiteDAOFactory

def instance_dao_factory(source: str):

    if not source:
        raise Exception("Missing source.")

    if source.startswith('sqlite'):
        _, file_path = source.split('::')
        return SQLiteDAOFactory(file_path)
    
    raise Exception("Invalid or missing source.")
    

def format_amount(amount: Decimal):
    return amount.quantize(Decimal("0.00"))

def as_json_list(objects):
    
    return '[%s]' % ','.join([obj.model_dump_json() for obj in objects])
        
