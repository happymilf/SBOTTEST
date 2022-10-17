from fastapi import FastAPI
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseSettings

from fastapi.logger import logger
##############


import os
import sys
from dotenv import load_dotenv
load_dotenv()

print()
class Settings(BaseSettings):
    # ... The rest of our FastAPI settings

    BASE_URL = os.getenv("BASE_URL")
    USE_NGROK = os.environ.get("USE_NGROK", "False") == "True"
    TOKEN = os.getenv("TOKEN")
    API_URL = f"https://api.telegram.org/bot"
    CHAT_ID = os.getenv("CHAT_ID")
    DATABASE_URL = os.getenv("DATABASE_URL")
settings = Settings()
from .utils.bot_utils import bot


def init_webhooks(base_url):
    # Update inbound traffic via APIs to use the public-facing ngrok URL
    pass
if settings.USE_NGROK:
    # pyngrok should only ever be installed or initialized in a dev environment when this flag is set
    from pyngrok import ngrok

    # Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
    # when starting the server
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000

    # Open a ngrok tunnel to the dev server
    public_url = ngrok.connect(port, bind_tls=True).public_url
    logger.info("ngrok tunnel \"{}\" -> \"https://127.0.0.1:{}\"".format(public_url, port))

    # Update any base URLs or webhooks to use the public ngrok URL
    settings.BASE_URL = public_url
    init_webhooks(public_url)

app : FastAPI = FastAPI()

WEBHOOK_PATH = f"bot/{settings.TOKEN}"
WEBHOOK_URL = settings.BASE_URL



@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )

@app.on_event("shutdown")
async def shutdown():
    await bot.session.close()



app.mount("/static", StaticFiles(directory="application/static"), name="static")



template : Jinja2Templates = Jinja2Templates("application/templates")


print(settings.BASE_URL)

os.system("curl --location --request POST \'https://api.telegram.org/bot" + settings.TOKEN +"/setWebhook\' --header \'Content-Type: application/json\' --data-raw \'{\"url\": \"" + settings.BASE_URL+"\"}\' ")

from .app_routes.admin import admin

#ROUTERS
app.include_router(admin.router)




####################################


from .app_routes.routes import (
    index,
)

app.add_route("/", index, name="index")
app.add_route("/admin", admin.admin_panel, name="admin")
app.add_route("/admin/users", admin.admin_panel_users, name="users")
app.add_route("/admin/bot", admin.admin_panel_users, name="bot")
app.add_route("/admin/user/{user_id}", admin.admin_panel_users, name="change_status")
app.add_route("/admin/promocodes", admin.admin_panel_users, name="promocodes")
app.add_route("/admin/delete_promo/{promo_id}", admin.admin_panel_users, name="delete_promo")


