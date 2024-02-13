from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base
from crud import get_user_email,create_user,get_users,get_user,get_items,create_item
from schemas import User,Item,UserCreate,ItemCreate


app = FastAPI()

Base.metadata.create_all(bind=engine)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/",response_model=User)
def creates_user(user:UserCreate,db:Session=Depends(get_db)):
    db_user= get_user_email(db,email=user.email)
    if db_user:
        raise HTTPException(status_code=400,detail="Email Already Exist")
    return create_user(db=db,user=user)

@app.get("/",response_model=list[User])
def gets_users(db:Session=Depends(get_db)):
    user=get_users(db)
    return user

@app.get("/user/{user_id}",response_model=User)
def get_user_by_id(user_id:int,db:Session =Depends(get_db)):
    dbuser=get_user(db,user_id=user_id)
    if dbuser is None:
        raise HTTPException(status_code=404,detail="User not found")
    return dbuser

@app.get("/items",response_model=list[Item])
def get_item(db:Session=Depends(get_db)):
    items = get_items(db)
    return items
@app.post("/users/{user_id}/item",response_model=Item)
def creates_item(user_id:int ,item:ItemCreate,db:Session=Depends(get_db)):
    return create_item(db=db,user_id=user_id,item=item)

@app.put("/update/{user_id}/",response_model=User)
def update_item(user:UserCreate,user_id : int ,db:Session=Depends(get_db)):
    db_user = get_user(db,user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not found")
    db_user.name=user.name
    db_user.email=user.email
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/delete/{user_id}",response_model=User)

def delete_user(user_id:int,db:Session=Depends(get_db)):
    db_user=get_user(db=db,user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return db_user




