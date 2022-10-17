from fastapi import APIRouter



router : APIRouter = APIRouter(
    prefix="/api",
    tags=["api"]
)


@router.get("/promocode")
def api_get_promo(id : int = None, username : str = None, status : str = None ):
    return {"Responce" : "OK"}


@router.post("/api/promocode")
def api_new_promo(text : str = None):
    return {"Responce" : "OK"}


@router.delete("/api/promocode")
def api_delete_promo(id : int):
    return {"Responce" : "OK"}



