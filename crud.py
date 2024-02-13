from sqlalchemy.orm import Session

import models,schemas

def get_user(db:Session,user_id:int):
    return db.query(models.User).filter(models.User.id==user_id).first()

def get_user_email(db:Session,email:str):
    return db.query(models.User).filter(models.User.email==email).first()

def get_users(db:Session):
    return db.query(models.User).all()

def create_user(db:Session,user:schemas.UserCreate):
    user = models.User(email=user.email,password=user.password,name=user.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_items(db:Session):
    return db.query(models.Item).all()


def create_item(db:Session,item:schemas.ItemCreate,user_id:int):
    item = models.Item(**item.dict(),owner_id=user_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item



