from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from flaskr.model import Base


class User(Base):

    __tablename__ = "users"
    last_refresh_date = ""

    id = Column(String, primary_key=True)
    name = Column(String)
    mycolor = Column(String, default="default")
    department = Column(String, default="Sales")
    maxrows = Column(Integer, default=500)
