from sqlalchemy import Column, Integer, String, Boolean
from db.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(250))
    available = Column(Boolean, default=True)
