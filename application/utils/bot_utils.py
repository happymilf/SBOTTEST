from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.dispatcher.filters import Text

from uuid import uuid4




from ..appcore import settings
from ..crud import (
    create_user,
    get_promo_user,
    get_user_status,
    change_user_status,
    check_user
    )
from .botdata import get_data

bot = Bot(token=settings.TOKEN)
dispatcher = Dispatcher(bot=bot)

  
@dispatcher.message_handler(commands="start")
async def start(message : types.Message):
    create_user(message.from_user.username)
    kb = [
        [types.KeyboardButton(text="ПОЛУЧИТЬ ПРОМОКОД")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(get_data("greetings"), reply_markup=keyboard)


@dispatcher.message_handler(Text("ПОЛУЧИТЬ ПРОМОКОД"))
async def promocode(message : types.Message): 
    result = await bot.get_chat_member(settings.CHAT_ID, message.from_user.id)
    if result["status"] == "left":
        print("LOL")
        await message.answer(get_data("check"))
    else:
        promocode = get_promo_user()
        if promocode == None:
            await message.answer(get_data("notokens"))
            return 0
        
        user = get_user_status(message.from_user.username)
        print(user)
        if promocode != "" and user == False:
            promocode_text = get_data("promo").replace("{promocode}", promocode)
            await message.answer(promocode_text)
            #get_data("promo") + f"\n{promocode}"
            change_user_status(username=message.from_user.username)
        else:
             await message.answer(get_data("already"))
           
        print("KEK")
   
    #r = requests.post(url)
    
@dispatcher.message_handler(commands="check")
async def check(message : types.Message):
    return 0
    