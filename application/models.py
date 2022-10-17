from .database import Base, engine

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    ForeignKey,
    Column
)
from sqlalchemy.orm import relationship 


class BotText(Base):
    __tablename__ = "bottexts"
    
    id : Column = Column(Integer, primary_key=True, index=True)
    field_name = Column(String(60), unique=True)
    field_text = Column(String(2000))
    
    


class User(Base):
    __tablename__ = "users"
    
    id : Column = Column(Integer, primary_key=True, index=True)
    username : Column = Column(String(50), unique=True)
    promocode : Column = Column(Boolean, default=False)
    
    
   
class PromoCode(Base):
    __tablename__ = "promocodes"
    
    id : Column = Column(Integer, primary_key=True, index=True)
    token : Column = Column(String(100), unique=True)
    is_active : Column = Column(Boolean, default=False)
    
    counter : Column = Column(Integer)


Base.metadata.create_all(bind=engine)