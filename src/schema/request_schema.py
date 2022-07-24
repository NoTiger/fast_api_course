from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str = ""  # not required is represented by providing default value
    available: bool = True

    class Config:
        orm_mode = True  # use this to enable pydantic to use ORM features
        schema_extra = {
            "example": {
                "name": "Item 1",
                "description": "This is item 1",
                "available": True,
            }
        }
