from fastapi import APIRouter

from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse


from fastapi import Request, Form, File, UploadFile

from application.utils.botdata import get_data, change_data


from ...appcore import template
from ...crud import get_users, add_promocode, get_promocodes, delete_promocode, change_user_status_byId


router : APIRouter = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@router.get("/")
def admin_panel(request : Request):


    return RedirectResponse("/admin/users", status_code=302)
    # return template.TemplateResponse(
    #     "admin/admin.html",
    #     context={
    #         "request" : request
    #         }
    #     )
    
@router.get("/users")
async def admin_panel_users(request : Request):
    users = get_users()
    print(users)
    return template.TemplateResponse(
        "admin/users/users.html",
        context={
            "request" : request,
            "users" : users,
            }
        )
@router.get("/user/{user_id}")
async def admin_panel_change_user(user_id : int):
    change_user_status_byId(user_id)
    return RedirectResponse("/admin/users", status_code=303)
    
@router.get("/promocodes" )
async def admin_panel_promocodes(request : Request):
    promocodes = get_promocodes()
    return template.TemplateResponse(
        "admin/promocodes/promocodes.html",
        context={
            "request" : request,
            "promocodes" : promocodes
            }
        )
    
@router.post("/promocodes")
async def admin_panel_add_promo(promocode : str = Form(), count : int = Form()):
    add_promocode(promocode=promocode, counter=count)
    return RedirectResponse("/admin/promocodes", status_code=303)
@router.post("/promocodes")
async def admin_panel_uploadfile(file : UploadFile = File(...)):
    pass
@router.get("/delete_promo/{promo_id}")
def delete_promo(promo_id : int ):
    delete_promocode(promo_id=promo_id)

    return RedirectResponse("/admin/promocodes", status_code=302)


@router.get("/bot")
async def admin_panel_bot( request : Request):

    return template.TemplateResponse(
        "admin/bot/bot.html",
        context={
            "request" : request,
            "greetings" : get_data("greetings"),
            "promo" : get_data("promo"),
            "check" : get_data("check"),
            "already" : get_data("already"),
            "notokens" : get_data("notokens"),
        }
    )

@router.post("/bot")
async def admin_bot_change_text(
        greetings : str = Form(),
        promo : str = Form(),
        check : str = Form(),
        already : str = Form(),
        notokens : str = Form(),
    ):
    change_data("greetings", greetings)
    change_data("promo", promo)
    change_data("check", check)
    change_data("already", already)
    change_data("notokens", notokens)
    return RedirectResponse("/admin/bot", status_code=302)

