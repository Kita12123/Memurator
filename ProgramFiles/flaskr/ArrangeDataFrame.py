"""
統計用モジュール
"""
import pandas as pd


def Totall(
    df: pd.DataFrame
    ) -> list[pd.DataFrame]:
    if df.empty:
        return (
            pd.DataFrame(index=[], columns=["ﾃﾞｰﾀﾅｼ"]),
            pd.DataFrame(index=[], columns=["ﾃﾞｰﾀﾅｼ"]),
            pd.DataFrame(index=[], columns=["ﾃﾞｰﾀﾅｼ"]))
    df = df[["伝票日付","数量","金額"]].copy()
    # Period
    def func(x):
        x = str(x)
        if len(x) != 8:
            return "0"
        else:
            return int(x[0:4]) + int(x[4:5]) - 1945
    df1 = df.copy()
    df1.loc[:,"期"] = df1["伝票日付"].map(func)
    df1 = df1[["期","数量","金額"]].groupby("期").sum()
    df1.insert(0, "期", value=df1.index)
    df1.loc[:,("数量","金額")] = df1[["数量","金額"]].applymap("{:,}".format)
    # Create Index
    df.loc[:,"伝票日付"] = pd.to_datetime(df["伝票日付"], format=r"%Y%m%d")
    df.set_index("伝票日付", inplace=True)
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

