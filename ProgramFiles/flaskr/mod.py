"""
統計用モジュール
"""
import os
import pandas as pd
from logging import (
    getLogger,
    StreamHandler,
    Formatter,
    FileHandler,
    handlers,
    Logger,
    DEBUG,
    INFO,
    ERROR,
    CRITICAL
)


#
# Sub Function
#
def year_to_period(date):
    date = str(date)
    if len(date) != 8:
        return "0"
    else:
        return int(date[0:4]) + int(date[4:5]) - 1945


#
# Main Function
#
def arrage_df(df: pd.DataFrame) -> list[pd.DataFrame]:
    if df.empty:
        return (
            pd.DataFrame(index=[], columns=["ﾃﾞｰﾀﾅｼ"]),
            pd.DataFrame(index=[], columns=["ﾃﾞｰﾀﾅｼ"]),
            pd.DataFrame(index=[], columns=["ﾃﾞｰﾀﾅｼ"]))
    df = df[["伝票日付", "数量", "金額"]].copy()
    df1 = df.copy()
    df1.loc[:, "期"] = df1["伝票日付"].map(year_to_period)
    df1 = df1[["期", "数量", "金額"]].groupby("期").sum()
    df1.insert(0, "期", value=df1.index)
    df1.loc[:, ("数量", "金額")] = df1[["数量", "金額"]].applymap("{:,}".format)
    # Create Index
    df.loc[:, "伝票日付"] = pd.to_datetime(df["伝票日付"], format=r"%Y%m%d")
    df.set_index("伝票日付", inplace=True)
    # Month
    df2 = df.copy().groupby(pd.Grouper(freq="1M")).sum()
    df2.insert(0, "伝票日付", value=df2.index)
    df2.loc[:, "伝票日付"] = df2["伝票日付"].dt.strftime(r"%Y/%m")
    df2.loc[:, ("数量", "金額")] = df2[["数量", "金額"]].applymap("{:,}".format)
    # Day
    df3 = df.copy().groupby(pd.Grouper(freq="1D")).sum()
    df3.insert(0, "伝票日付", value=df3.index)
    df3.loc[:, "伝票日付"] = df3["伝票日付"].dt.strftime(r"%Y/%m/%d")
    df3.loc[:, ("数量", "金額")] = df3[["数量", "金額"]].applymap("{:,}".format)
    return df1, df2, df3


#
# Main Class
#
class Log:
    """ログ管理クラス"""
    def __init__(self, folder: str, toaddrs: list[str]) -> None:
        """
        Args:
            folder (str): ログファイル出力フォルダ
            toaddrs (list): メール送信先アドレスリスト
        """
        self.folder = folder
        if type(toaddrs) != list:
            self.toaddrs = list(toaddrs)
        else:
            self.toaddrs = toaddrs
        self.formater = Formatter("[%(levelname)s]%(asctime)s-%(message)s")

    @property
    def handler_default(self) -> StreamHandler:
        handler = StreamHandler()
        handler.setLevel(DEBUG)
        handler.setFormatter(self.formater)
        return handler

    @property
    def handler_debug_file(self) -> FileHandler:
        """Output debug.txt"""
        handler = FileHandler(
            os.path.join(self.folder, "debug.txt"),
            mode="w",
            encoding="utf-8"
        )
        handler.setLevel(DEBUG)
        handler.setFormatter(self.formater)
        return handler

    @property
    def handler_info_file(self) -> FileHandler:
        """Output info.txt"""
        handler = FileHandler(
            os.path.join(self.folder, "info.txt"),
            mode="w",
            encoding="utf-8"
        )
        handler.setLevel(INFO)
        handler.setFormatter(self.formater)
        return handler

    @property
    def handler_error_file(self) -> FileHandler:
        """Output info.txt"""
        handler = FileHandler(
            os.path.join(self.folder, "error.txt"),
            mode="w",
            encoding="utf-8"
        )
        handler.setLevel(ERROR)
        handler.setFormatter(self.formater)
        return handler

    @property
    def handler_critical_mail(self) -> handlers.SMTPHandler:
        handler = handlers.SMTPHandler(
            mailhost="127.0.0.1",
            fromaddr="server-error@example.com",
            toaddrs=self.toaddrs,
            subject="Application Error"
        )
        handler.setLevel(CRITICAL)
        handler.setFormatter(self.formater)
        return handler

    def create_logger(self) -> Logger:
        """"""
        logger = getLogger("__main__")
        logger.setLevel(DEBUG)
        logger.addHandler(self.handler_debug_file)
        logger.addHandler(self.handler_info_file)
        logger.addHandler(self.handler_error_file)
        return logger
