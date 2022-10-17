from fastapi import Depends

from sqlalchemy.orm import Session
from sqlalchemy import func

from .models import User, PromoCode

from .database import get_database, SessionLocal

def create_user(username : str , db : Session = SessionLocal()):
    if db.query(User).filter_by(username=username).first() is None:
        user = User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)
def check_user(username : str, db : Session = SessionLocal()):
    if db.query(User).filter_by(username=username).first() is not None:
        return True
    else:
        return False
def get_users(db : Session = SessionLocal()):
    users = db.query(User).all()
    if users is not None:
        return users
    else:
        return False
        
def get_user_status(username : str, db : Session = SessionLocal()):
    user : User = db.query(User).filter_by(username=username).first()
    return user.promocode

def change_user_status(username : str, db : Session = SessionLocal()):
    user : User = db.query(User).filter_by(username=username).first()
    if user is None:
        new_user : User = User(username=username, promocode=True)
        db.add(new_user)
        db.commit()
        db.refresh()
    else:   
        user.promocode = not user.promocode
        db.commit()
def change_user_status_byId(id : int, db : Session = SessionLocal()):
    user : User = db.query(User).filter_by(id=id).first()
    if user is None:
        new_user : User = User(username=id, promocode=True)
        db.add(new_user)
        db.commit()
        db.refresh()
    else:   
        user.promocode = not user.promocode
        db.commit()
def add_promocode(promocode : str,counter : int, db : Session = SessionLocal()):
    promocode : PromoCode = PromoCode(token=promocode, counter=counter, is_active=True)
    
    db.add(promocode)
    db.commit()
    db.refresh(promocode)
  
  
    
def get_promocodes(db : Session = SessionLocal()):
    return db.query(PromoCode).all()


def get_promo_user(db : Session = SessionLocal()):
    counter_min = db.query(func.min(PromoCode.counter)).scalar()
    promo : PromoCode = db.query(PromoCode).filter_by(counter=counter_min).first()
    if promo != None:    
        if promo.counter !=0:
            promo.counter-=1
            db.commit()
            
            return promo.token
        else:
            db.query(PromoCode).filter_by(counter=0).delete()
            db.commit()
            return False
            
    
    
def delete_promocode(promo_id : int, db : Session = SessionLocal()):
    db.query(PromoCode).filter_by(id=promo_id).delete()
    db.commit()
    
    
    
def get_bot_text(field_name : str, db : SessionLocal()):
    pass