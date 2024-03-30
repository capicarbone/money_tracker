
from decimal import Decimal


def format_amount(amount: Decimal):
    return amount.quantize(Decimal("0.00"))
        
