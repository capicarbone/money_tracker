from datetime import date
from uuid import uuid4
from decimal import Decimal

from typing import List
from pydantic import BaseModel
from money_tracker.models import *
from money_tracker.daos.base import DataAccessObject, AbsTransactionsDAO, AbsAccountsDAO

global_simple_storage = {}

class BaseInMemoryDao(DataAccessObject):
      
    storage_name = None

    @property
    def __memory_storage(self):
        if self.storage_name not in global_simple_storage:
            global_simple_storage[self.storage_name] = {}

        return global_simple_storage[self.storage_name]
      
    def save(self, entity: BaseModel) -> BaseModel:
        entity.id = str(uuid4()) if not entity.id else entity.id
        self.__memory_storage[entity.id] = entity
        return entity

    def exists(self, entity_id: str) -> bool:
        return entity_id in self.__memory_storage

    def delete(self, entity_id: str):
        if self.exists(entity_id):
            del(self.__memory_storage[entity_id])

    def update(self, entity: BaseModel):
        if self.exists(entity.id):
            self.__memory_storage[entity.id] = entity

    def get(self, entity_id: str) -> BaseModel:
        return self.__memory_storage[entity_id]
    
    def clear(self):
        global_simple_storage[self.storage_name].clear()


class GetAll:
    
    def get_all(self):
        return list(global_simple_storage[self.storage_name].values())
    

# Implementations

class InMemoryTransactionsDAO(BaseInMemoryDao, AbsTransactionsDAO):

    storage_name = 'transactions'

    def get_transactions(self, account_id: str, start_date: date, end_date: date, limit: int, offset: int) -> List[Transaction]:
        
        filtered_items = global_simple_storage[self.storage_name].values()        

        if account_id:
            filtered_items = filter(lambda x: x.account_id == account_id, filtered_items)

        return list(filtered_items)

    def save_many(self, transactions: List[Transaction]):
        for t in transactions:
            self.save(t)


class InMemoryAccountsDAO(GetAll, BaseInMemoryDao, AbsAccountsDAO):

    storage_name = 'accounts'

    def update_balance(self, account_id:str, balance: Decimal):
        pass

class InMemoryTransactionCategoriesDAO(BaseInMemoryDao, AbsTransactionsDAO, GetAll):

    storage_name = 'categories'
    