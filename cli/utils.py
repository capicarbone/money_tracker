
from decimal import Decimal


def format_amount(amount: Decimal):
    return amount.quantize(Decimal("0.00"))

def as_json_list(objects):
    
    return '[%s]' % ','.join([obj.model_dump_json() for obj in objects])
        
