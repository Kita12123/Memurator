"""
Query作成（マスタ検索用）
"""
from ProgramFiles.query import ( 
    seihinbuhin,
    soukasaki,
    tokuisaki,
    zatu,
    denk,
    tantou
)

class MASTER_CLS:
    def __init__(self):
        """抽出対象の列名"""
        self.query_columns = [
            "カナ名",
            "名称",
            "担当者名",
            "住所",
            "部番"
            ]

    def create_selects(self, column: str, value: str):
        def func(c :str) -> list[str]:
            """調整する"""
            c = c.replace(" ","")
            if c.isdigit() == False:
                return []
            c = str(int(c))
            if column == "得意先":
                if len(c) < 5:
                    return [f"{c}10", f"{c}20", f"{c}40"]
            #elif column == "製品部品":
            #    if len(c) == 5:
            #        [c + str(i).zfill(2) for i in range(100)]
            return [c]
        if value == "":
            return []
        elif "," not in value:
            return func(value)
        result = []
        for s in value.split(","):
            result += func(s)     
        return result
    
    def create_sql_dsp(self, column, form_dic: dict[str,str]):
        """SQL（表示用）作成"""
        where = self.create_where(form_dic=form_dic)
        if column == "得意先":
            return tokuisaki.Create_SQL_dsp(
                where=where
            )
        elif column == "送荷先":
            return soukasaki.Create_SQL_dsp(
                where=where
            )
        elif column == "雑":
            return zatu.Create_SQL_dsp(
                where=where
            )
        elif column == "製品部品":
            return seihinbuhin.Create_SQL_dsp(
                where=where
            )
        elif column == "担当者":
            return tantou.Create_SQL_dsp(
                where=where
            )
        elif column == "伝票区分":
            return denk.Create_SQL_dsp(
                where=where
            )

    def create_sql_download(self, column, form_dic: dict[str,str]={}):
        """SQL（ダウンロード用）作成"""
        where = self.create_where(form_dic=form_dic)
        if column == "得意先":
            return tokuisaki.Create_SQL_download(
                where=where
            )
        elif column == "送荷先":
            return soukasaki.Create_SQL_download(
                where=where
            )
        elif column == "雑":
            return zatu.Create_SQL_download(
                where=where
            )
        elif column == "製品部品":
            return seihinbuhin.Create_SQL_download(
                where=where
            )
        elif column == "担当者":
            return tantou.Create_SQL_download(
                where=where
            )
        elif column == "伝票区分":
            return denk.Create_SQL_download(
                where=where
            )

    def create_where(self, form_dic: dict[str,str]):
        """SQL WHERE句作成"""
        where = ""
        for name in self.query_columns:
            if name in form_dic and form_dic[name]:
                where += f"{name} LIKE'%{form_dic[name]}%' AND "
        if where == "":
            return ""
        else:
            return where[:-5]



MASTER = MASTER_CLS()