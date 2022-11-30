"""
Query作成
"""
import os
from functools import cache

from ProgramFiles.query import mod

CD = os.path.dirname(__file__)


# メモリ節約
@cache
def ReadSqlFile(
    db_name: dict,
    download: bool
) -> str:
    """SQLコード作成"""
    if download:
        cd = os.path.join(CD, "Download")
    else:
        cd = os.path.join(CD, "Display")
    with open(
        os.path.join(cd, db_name+".txt"),
        mode="r",
        encoding="utf-8"
    ) as f:
        return f.read()


def CreateWhereCode(query: dict):
    db_name = query["データ名"]
    if db_name == "売上データ" or db_name == "出荷データ":
        # 各WHERE句を <> AND で結合させ、[:-4]で最後のANDを削除
        return "".join([f"{q} AND " for q in [
            mod.Equal("得意先コード", "得意先カナ", query["得意先"]),
            mod.Equal("送荷先コード", "送荷先カナ", query["送荷先"]),
            mod.Equal("雑コード", "雑カナ", query["雑"]),
            mod.Equal("製品部品コード", "製品部品カナ", query["製品部品"]),
            mod.Equal("担当者コード", "担当者名＊", query["担当者"]),
            mod.Equal("伝票区分", "伝票区分名＊", query["伝票区分"]),
            mod.GreaterEqual("伝票日付", query["開始日付"]),
            mod.LessEqual("伝票日付", query["終了日付"]),
            mod.Flag(query["製品部品フラグ"]),
        ] if q])[:-4]
    elif db_name == "仕入データ":
        return "".join([f"{q} AND " for q in [
            mod.Equal("仕入先コード", "仕入先カナ", query["手配先"]),
            mod.Equal("品目コード", "品目カナ", query["品目"]),
            mod.GreaterEqual("伝票日付", query["開始日付"]),
            mod.LessEqual("伝票日付", query["終了日付"])
        ] if q])[:-4]
    elif db_name == "定期注文データ":
        return "".join([f"{q} AND " for q in [
            mod.Equal("手配先コード", "手配先名", query["手配先"]),
            mod.Equal("品目コード", "品目カナ", query["品目"]),
            mod.GreaterEqual("納期", query["開始日付"]),
            mod.LessEqual("納期", query["終了日付"])
        ] if q])[:-4]
    else:
        return "1=1"


def CreateWhereCodeMaster(query: dict):
    if query:
        return "".join(
            [f"{mod.Equal(c, c, query[c])} AND " for c in query.keys()]
        )[:-4]
    else:
        return "1=1"


def CreateSqlCode(query: dict, download: bool):
    where = CreateWhereCode(query)
    # SQLにWHERE句を書き込んでいるため
    if where == "":
        where = "1=1"
    return ReadSqlFile(
        db_name=query["データ名"],
        download=download
        ).format(where)


def SelectList(column: str, value: str) -> list[str]:
    def func(c: str) -> list[str]:
        """調整する"""
        c = c.replace(" ", "")
        if not c.isdigit():
            return [c]
        c = int(c)
        if column == "得意先":
            if len(str(c)) < 5:
                return [f"{c}10", f"{c}20", f"{c}40"]
            else:
                [str(c)]
        return [c]
    if value == "":
        return []
    elif "," not in value:
        return func(value)
    result = []
    for s in value.split(","):
        result += func(s)
    return result
