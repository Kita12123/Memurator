"""
Database Package
"""
from ProgramFiles.db import func

#
# Main
#
def create_uriage_df(
    sql_where_sqlite3: str,
    sort_column: str,
    sort_type: str
    ) -> tuple[func.pd.DataFrame, str]:
    # データ取得
    sql=func.craft_sql(
        sql_where_sqlite3=sql_where_sqlite3,
        sort_column=sort_column,
        sort_type=sort_type
    )
    df = func.create_df_sqlite3(
        sql=sql
    )
    return df, sql