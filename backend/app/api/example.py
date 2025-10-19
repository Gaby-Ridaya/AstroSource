from fastapi import APIRouter

router = APIRouter(prefix="/example", tags=["example"])

@router.get("/")
def read_example():
    return {"msg": "Ceci est une route d'exemple."}
