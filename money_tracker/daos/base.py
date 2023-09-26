from datetime import date
from pydantic import BaseModel

from models import Account, Transaction, Category

class DataAccessObject:
    
    def exists(entity_id: str) -> bool:
        raise NotImplementedError()
    
    def save(entity: BaseModel) -> BaseModel:
        raise NotImplementedError()
    
    def delete(entity: BaseModel):
        raise NotImplementedError()
    
    def update(entity: BaseModel):
        raise NotImplementedError()
    

class AbsTransactionsDAO(DataAccessObject):

    def get_transactions(account_id: str, start_date: date, end_date: date, limit: int, offset: int) -> List[Transaction]:
        raise NotImplementedError()
    
class AbsAccountsDAO(DataAccessObject):
    def get_all() -> List[Account]:
        raise NotImplementedError()
    
class AbsTransactionCategoriesDAO(DataAccessObject):
    def get_all() -> List[Category]:
        raise NotImplementedError()
    

    
