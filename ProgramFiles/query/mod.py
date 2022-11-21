"""
WHERE句作成
"""

def Equal(
    column_int: str,
    column_str: str,
    value: str
    ):
    """WHERE句作成(=)"""
    def func(v: str):
        # マスタ用にcolumn_int=""であれば、飛ばす
        if v.isdigit() and column_int:
            # 開始日付の対応
            if column_int == "開始日付":
                return f"伝票日付>={int(value.replace('-','')) - 19500000}"
            # 終了日付の対応
            if column_int == "終了日付":
                return f"伝票日付<={int(value.replace('-','')) - 19500000}"
            # 得意先の連番対応
            if column_int == "得意先コード" and len(v) <= 4:
                # 4ｹﾀ未満でも対応する
                z = '0'*(4 - len(v))
                return f"OR ( 得意先コード>={z}{v}00 AND 得意先コード<={z}{v}99 )"
            # 製品の連番対応
            elif column_int == "製品部品コード" and len(v) == 5:
                return f"OR ( 製品部品コード>={v}00 AND 製品部品コード<={v}99 )"
            else:
                return f"OR {column_int}={v} "
        else:
            return f"OR {column_str} LIKE'%{v}%' "
    v = value.replace(" ","")
    if v == "":
        return "1=1"
    if "," in v:
        # [2:]で初期の"OR"を削除
        return "(" + "".join([ func(code) for code in v.split(",")])[2:] + ")"
    else:
        return func(v)[2:]

def GreaterEqual(
    column_int: str,
    value: str
    ):
    """WHERE句作成(>=)"""
    v = value.replace(" ","")
    if v == "":
        return
    # 日付の対応
    if column_int == "伝票日付":
        return f"伝票日付>={int(v.replace('-','')) - 19500000}"
    else:
        return f"{column_int}>={v}"

def LessEqual(
    column_int: str,
    value: str
    ):
    """WHERE句作成(<=)"""
    v = value.replace(" ","")
    if v == "":
        return
    # 日付の対応
    if column_int == "伝票日付":
        return f"伝票日付<={int(v.replace('-','')) - 19500000}"
    else:
        return f"{column_int}<={v}"

def Flag(
    flag: str
    ):
    if   flag == "製品のみ":
        return "製品部品コード< 10000000"
    elif flag == "部品のみ":
        return "製品部品コード>=10000000"
    else:
        return "1=1"