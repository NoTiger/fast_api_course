from typing import List

from fastapi import Depends, Response, status, APIRouter

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false
from db.database import get_db
from db import db_schema
from schema import request_schema

router = APIRouter(prefix="/item", tags=["Item"])

# Order of router path matters
# if place underneath /items/{item_id}, it will not be matched first
@router.get("/unavailable", response_model=List[request_schema.Item])
def read_unavailable_item(db_session: Session = Depends(get_db)):
    """
    @summary: show all unavailable items
    """
    items = (
        db_session.query(db_schema.Item)
        .filter(db_schema.Item.available == false())
        .all()
    )

    return items


@router.get("/{item_id}", response_model=request_schema.Item)
def read_item(
    item_id: int, db_session: Session = Depends(get_db), response: Response = Response
):
    """
    @summary: show item by id
    @param item_id: id of item
    """
    item = db_session.query(db_schema.Item).filter(db_schema.Item.id == item_id).first()

    if not item:
        response.status_code = status.HTTP_404_NOT_FOUND

    return item


@router.get("/", response_model=List[request_schema.Item])
def read_items(
    available: bool = True,
    skip: int = 0,
    limit: int = 10,
    db_session: Session = Depends(get_db),
):
    """
    @summary: show all items
    """
    items = (
        db_session.query(db_schema.Item)
        .filter(db_schema.Item.available == available)
        .order_by(db_schema.Item.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return items


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=request_schema.Item,
)
def create_item(item: request_schema.Item, db_session: Session = Depends(get_db)):
    """
    @summary: create item
    """
    new_item = db_schema.Item(**item.dict())

    db_session.add(new_item)
    db_session.commit()
    db_session.refresh(new_item)

    return new_item


@router.put("/{item_id}", response_model=request_schema.Item)
def update_item(
    item_id: int, item: request_schema.Item, db_session: Session = Depends(get_db)
):
    """
    @summary: update item by id
    @param item_id: id of item
    """
    item_to_update = (
        db_session.query(db_schema.Item).filter(db_schema.Item.id == item_id).first()
    )

    if item_to_update:
        item_to_update.name = item.name
        item_to_update.description = item.description
        item_to_update.available = item.available

        db_session.commit()

        return item_to_update

    return Response(status_code=404)


@router.delete("/{item_id}")
def delete_item(item_id: int, db_session: Session = Depends(get_db)):
    """
    @summary: delete item by id
    @param item_id: id of item
    """
    item_to_delete = (
        db_session.query(db_schema.Item).filter(db_schema.Item.id == item_id).first()
    )

    if item_to_delete:
        db_session.delete(item_to_delete)
        db_session.commit()

        return Response(status_code=204)

    return Response(status_code=404)
