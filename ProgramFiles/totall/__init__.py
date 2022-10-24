"""
統計Module
"""
import pandas as pd

class Totall_CLS:
    def __init__(self):
        self.table = None
        self.columns = ["伝票日付","数量","金額"]
        self.values = ["数量","金額"]

    def create(
        self,
        df: pd.DataFrame
        ) -> list[pd.DataFrame]:
        if df.empty:
            return (
                pd.DataFrame(index=[], columns=["ﾃﾞｰﾀﾅｼ"]),
                pd.DataFrame(index=[], columns=["ﾃﾞｰﾀﾅｼ"]),
                pd.DataFrame(index=[], columns=["ﾃﾞｰﾀﾅｼ"]))
        df = df[self.columns].copy()
        df.loc[:,"伝票日付"] = pd.to_datetime(df["伝票日付"], format=r"%Y%m%d")
        df.set_index("伝票日付", inplace=True)
        # Year
        df1 = df.copy().groupby(pd.Grouper(freq="1Y")).sum()
        df1.insert(0, "伝票日付", value=df1.index)
        df1.loc[:,"伝票日付"] = df1["伝票日付"].dt.strftime(r"%Y")
        df1.loc[:,("数量","金額")] = df1[["数量","金額"]].applymap("{:,}".format)
        # Month
        df2 = df.copy().groupby(pd.Grouper(freq="1M")).sum()
        df2.insert(0, "伝票日付", value=df2.index)
        df2.loc[:,"伝票日付"] = df2["伝票日付"].dt.strftime(r"%Y/%m")
        df2.loc[:,("数量","金額")] = df2[["数量","金額"]].applymap("{:,}".format)
        # Day
        df3 = df.copy().groupby(pd.Grouper(freq="1D")).sum()
        df3.insert(0, "伝票日付", value=df3.index)
        df3.loc[:,"伝票日付"] = df3["伝票日付"].dt.strftime(r"%Y/%m/%d")
        df3.loc[:,("数量","金額")] = df3[["数量","金額"]].applymap("{:,}".format)
        return df1, df2, df3

    def adjust_selects(
        self,
        selects
        ) -> tuple[list, list]:
        """抽出列, Groupbyのbyパラメータ作成"""
        columns = []
        by = []
        for s in selects:
            if   s == "1年":
                by.append(pd.Grouper(freq="1Y"))
                columns.append("伝票日付")
            elif s == "1か月":
                by.append(pd.Grouper(freq="1M"))
                columns.append("伝票日付")
            elif s == "1週間":
                by.append(pd.Grouper(freq="1W"))
                columns.append("伝票日付")
            elif s == "1日":
                by.append(pd.Grouper(freq="1D"))
                columns.append("伝票日付")
            elif s == "得意先":
                by += ["得意先コード","得意先カナ"]
                columns += ["得意先コード","得意先カナ"]
            elif s == "送荷先":
                by += ["送荷先コード","送荷先カナ"]
                columns += ["送荷先コード","送荷先カナ"]
            elif s == "製品部品":
                by += ["製品部品コード","製品部品カナ"]
                columns += ["製品部品コード","製品部品カナ"]
            else:
                by.append(s)
                columns.append(s)
            continue
        return columns, by

TOTALL = Totall_CLS()