import types
from typing import Any
import couchdb

class DbModel:
    def __init__(self, entity) -> None:
        self.id = entity['id']
        self.field = entity['field']

    def __str__(self) -> str:
        return f"'id': {self.id}, 'field': {self.field}"
    
host = 'db'
port = 5984
username = 'maria'
password = 'pass'

def select_obj(r):
    enitity = DbModel(r)
    print(enitity.__dict__)
    return enitity.__dict__

def select_all(doc):
    # select all
    for d in doc:
        doc_id = d
        o = doc[doc_id]
        select_obj(o)

def main():
    couch = couchdb.Server(f'http://{username}:{password}@{host}:{port}')
    db = couch.create('test') # newly created

    # insert
    doc = [
        {'id': 1, 'field': 'red'},
        {'id': 2, 'field': 'blue'},
        {'id': 3, 'field': 'green'}
    ]
    for r in doc:
        db.save(r)
    
    print("select all")
    select_all(db)

    print("filter by")
    for r in db.find({'selector': {'id': 1}}):
        select_obj(r)

    print("filter by range")
    # filter by range
    for r in db.find({'selector': {'id': {'$gt': 1}}}):
        select_obj(r)

    print("update")
    for r in db.find({'selector': {'id': 1}}):
        d = select_obj(r)
        d['field'] = 'updated'
        db.save(d)

    select_all(db)

    # delete
    for r in doc:
        db.delete(r)
    couch.delete('test')

if __name__ == "__main__":
    main()