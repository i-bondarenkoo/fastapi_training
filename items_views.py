from fastapi import Path

from fastapi import APIRouter

#вынесли в отдельное пространство views/представления которые 
#касаются отдельной группы
router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/")
def list_items():
    return [
        "Item1",
        "Item2",
        "Item3",
    ]   


@router.get("/latest/")
def get_latest_item():
    return {"item": {"id": "0", "name": "latest"}}    


#item_id параметр пути
@router.get("/{item_id}/")
def get_item_by_id(item_id: int = Path(..., ge=1, lt=100000)):
    return {
        "Item": {
            'id': item_id,
        },
    }
    