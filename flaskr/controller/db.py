
from flaskr.model import Session
from flaskr.model.database import *


def create_sales_data():
    with Session() as session, session.begin():
        session.query(
            SoldTotalData
        )