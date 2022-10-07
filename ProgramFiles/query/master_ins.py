"""
Query作成（マスタ検索用）
"""
from ProgramFiles.query import ( 
    soukasaki,
    tokuisaki,
    zatu
)

class MASTER_CLS:
    def __init__(self):
        """抽出対象の列名"""
        self.query_columns = [
            "カナ名",
            "名称",
            "担当者名",
            "住所"
            ]

    def create_selects(self, column: str, value: str):
        selects = value.split(",")
        selects_ = selects
        for s in selects_:
            selects.remove(s)
            s_ = str(s).replace(" ","")
            if s_.isdigit() == False:
                continue
            elif column == "得意先":
                s_ = int(s_)
                if len(str(s_)) < 5:
                    selects += [f"{s_}10", f"{s_}20", f"{s_}40"]
                else:
                    selects += [str(s_)]
        return selects
    
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

    def create_sql_download(self, column, form_dic: dict[str,str]):
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