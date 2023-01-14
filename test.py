# .pycを作成しない
import sys
sys.dont_write_bytecode = True

from flaskr.common.model.crud.create import sync_host_all, sync_host
from flaskr.common.model.crud.read import create_df


def test_sync_host():
    sync_host(
        "earnings",
        first_date=721228
    )

def test_sync_host_all():
    sync_host_all(
        first_date=730100
    )

def test_create_df():
    df = create_df(
        filename="sales",
        tablename="shippings",
        where="伝票日付 == 20230105")
    return df




if __name__=="__main__":
    #test_sync_host_all()
    df = test_create_df()
    print(df)
    se = df.sum("金額")
    print(se)