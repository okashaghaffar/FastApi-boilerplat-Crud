from sqlalchemy import Boolean,Column,ForeignKey,Integer,String
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__="users"
    id = Column(Integer,primary_key=True)
    name=Column(String)
    email= Column(String,unique=True,index=True)
    password=Column(String)
    is_active=Column(Boolean,default=True)
    #here owners refer to owner variable in class item
    items=relationship("Item",back_populates="owner")

class Item(Base):
    __tablename__="items"
    id = Column(Integer,primary_key=True)
    title = Column(String)
    description = Column(String)
    owner_id = Column(Integer,ForeignKey("users.id"))

    owner = relationship("User",back_populates="items")