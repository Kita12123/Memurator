# .pycを作成しない
import sys
sys.dont_write_bytecode = True

from flaskr.model.crud import sync_host
from flaskr.model import Session
from flaskr.model.database import *


def test_sync():
    sync_host.sync_host("customer_codes")
    with Session() as session, session.begin():
        results : list[CustomerCodeMaster] = session.query(CustomerCodeMaster).filter(
            CustomerCodeMaster.customer_code==10000
        ).all()
        print(results[0].customer_code)
        print(results[0].address)

test_sync()