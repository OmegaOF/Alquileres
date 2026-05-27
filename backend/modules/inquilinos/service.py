from sqlalchemy.orm import Session
from modules.inquilinos.models import Inquilino
def list_items(db:Session): return db.query(Inquilino).all()
def get_item(db:Session,item_id:int): return db.get(Inquilino,item_id)
def create_item(db:Session,payload): i=Inquilino(**payload.model_dump(exclude_unset=True)); db.add(i); db.commit(); db.refresh(i); return i
def update_item(db:Session,item,payload):
 for k,v in payload.model_dump(exclude_unset=True).items(): setattr(item,k,v)
 db.commit(); db.refresh(item); return item
def delete_item(db:Session,item): db.delete(item); db.commit()
