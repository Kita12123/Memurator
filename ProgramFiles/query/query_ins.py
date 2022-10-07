"""
Query作成
"""
from ProgramFiles.flaskr.user_ins import USER
from ProgramFiles.query import ( 
    syukka,
    uriage,
    tokuisaki
)

class QUERY_CLS:
    
    def create_sql_dsp(self, ip, db_name, where=""):
        user_query = USER.load(ip=ip)
        if db_name == "売上データ":
            return uriage.Create_SQL_dsp(
                where=self.create_where(ip=ip),
                sort_column=user_query["順列"],
                sort_type=user_query["順列タイプ"]
            )
        elif db_name == "出荷データ":
            return syukka.Create_SQL_dsp(
                where=self.create_where(ip=ip),
                sort_column=user_query["順列"],
                sort_type=user_query["順列タイプ"]
            )
        elif db_name == "得意先":
            return tokuisaki.Create_SQL_dsp(
                where=where
            )

    def create_sql_download(self, ip, db_name, where=""):
        user_query = USER.load(ip=ip)
        if db_name == "売上データ":
            return uriage.Create_SQL_download(
                where=self.create_where(ip=ip),
                sort_column=user_query["順列"],
                sort_type=user_query["順列タイプ"]
            )
        elif db_name == "出荷データ":
            return syukka.Create_SQL_download(
                where=self.create_where(ip=ip),
                sort_column=user_query["順列"],
                sort_type=user_query["順列タイプ"]
            )
        elif db_name == "得意先":
            return tokuisaki.Create_SQL_dsp(
                where=where
            )
    
    def create_where(self, ip):
        """SQL WHERE句作成"""
        user_query = USER.load(ip=ip)
        # 開始日付
        if "開始日付" not in user_query:
            first_date = ""
        if user_query["開始日付"] == "":
            first_date = ""  
        else:
            fd_ = int(user_query["開始日付"].replace("-","")) - 19500000
            first_date = f" 伝票日付>={fd_} AND\n"
        # 終了日付
        if "終了日付" not in user_query:
            last_date = ""
        elif user_query["終了日付"] == "":
            last_date = ""
        else:
            ld_ = int(user_query["終了日付"].replace("-","")) - 19500000
            last_date = f" 伝票日付<={ld_} AND\n"
        # 製品部品
        def func(c: str):
            c = c.replace(" ", "")
            if c.isdigit():
                if len(c) == 5:
                    return f" OR ( 製品部品コード>={c}00 AND 製品部品コード<={c}99 ) "
                return f" OR 製品部品コード={c} "
            else:
                return f" OR 製品部品カナ LIKE'%{c}%' "
        if "製品部品" not in user_query:
            seihinbuhin = ""
        elif user_query["製品部品"] == "":
            seihinbuhin = ""
        elif "," in user_query["製品部品"]:
            # ','区切りにORで結合した、SQLコードを作成する
            sql = "".join([func(code) for code in user_query["製品部品"].split(",")])[3:]
            seihinbuhin = f" ({sql}) AND\n"
        else:
            seihinbuhin = func(user_query["製品部品"])[3:] + " AND\n"
        # 製品部品フラグ
        if "製品部品フラグ" not in user_query:
            seihinbuhin2 = ""
        elif user_query["製品部品"] == "":
            seihinbuhin2 = ""
        elif user_query["製品部品フラグ"] == "seihin":
            seihinbuhin2 = " 製品部品コード<= 9999999 AND \n"
        #elif user_query["製品部品フラグ"] == "buhin":
        else:
            seihinbuhin2 = " 製品部品コード>=10000000 AND \n"
        # 得意先
        def func(c: str):
            c = c.replace(" ", "")
            if c.isdigit():
                if len(c) <= 4:
                    # 3ｹﾀでも対応する
                    z = '0'*(4 - len(c))
                    return f" OR ( 得意先コード>={z}{c}00 AND 得意先コード<={z}{c}99 ) "
                return f" OR 得意先コード={c} "
            else:
                return f" OR 得意先カナ LIKE'%{c}%' "
        if "得意先" not in user_query:
            tokuisaki = ""
        elif user_query["得意先"] == "":
            tokuisaki = ""
        elif "," in user_query["得意先"]:
            sql = "".join([ func(code) for code in user_query["得意先"].split(",")])[3:]
            tokuisaki = f" ({sql}) AND\n"
        else:
            tokuisaki = func(user_query["得意先"])[3:] + " AND \n"
        # 送荷先
        def func(c: str):
            c = c.replace(" ", "")
            if c.isdigit():
                return f" OR 送荷先コード={c} "
            else:
                return f" OR 送荷先カナ LIKE'%{c}%' "
        if "送荷先" not in user_query:
            soukasaki = ""
        elif user_query["送荷先"] == "":
            soukasaki = ""
        elif "," in user_query["送荷先"]:
            sql = "".join([ func(code) for code in user_query["送荷先"].split(",")])[3:]
            soukasaki = f" ({sql}) AND\n"
        else:
            soukasaki = func(user_query["送荷先"])[3:] + " AND \n"
        # 雑
        def func(c: str):
            c = c.replace(" ", "")
            if c.isdigit():
                return f" OR 雑コード={c} "
            else:
                return f" OR 雑カナ＊ LIKE'%{c}%' "
        if "雑" not in user_query:
            zatu = ""
        elif user_query["雑"] == "":
            zatu = ""
        elif "," in user_query["雑"]:
            sql = "".join([ func(code) for code in user_query["雑"].split(",")])[3:]
            zatu = f" ({sql}) AND\n"
        else:
            zatu = func(user_query["雑"])[3:] + " AND \n"
        # 担当者
        def func(c: str):
            c = c.replace(" ", "")
            if c.isdigit():
                return f" OR 担当者コード={c} "
            else:
                return f" OR 担当者名＊ LIKE'%{c}%' "
        if "担当者" not in user_query:
            tantou = ""
        elif user_query["担当者"] == "":
            tantou = ""
        elif "," in user_query["担当者"]:
            sql = "".join([ func(code) for code in user_query["担当者"].split(",")])[3:]
            tantou = f" ({sql}) AND\n"
        else:
            tantou = func(user_query["担当者"])[3:] + " AND \n"
        return (
            first_date
        +   last_date
        +   seihinbuhin
        +   seihinbuhin2
        +   tokuisaki
        +   zatu
        +   soukasaki
        +   tantou
        )[:-5]

QUERY = QUERY_CLS()