from ..appcore import app, WEBHOOK_PATH
#########################
from fastapi import Request, Depends

from fastapi.responses import JSONResponse

from aiogram import Dispatcher, types, Bot

from sqlalchemy.orm import Session

from application.utils.bot_utils import bot, dispatcher
from fastapi.responses import RedirectResponse
from ..database import get_database
from ..models import User

@app.get("/")
def index():
    return RedirectResponse("/admin/users", status_code=302)

@app.post("/")
async def bot_webhook(update : dict):
    print(update)
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dispatcher)
    Bot.set_current(bot)
    await dispatcher.process_update(telegram_update)
    
    
    

