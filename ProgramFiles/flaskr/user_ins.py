"""
ユーザー入力管理
"""
import json
from datetime import datetime, timedelta

from ProgramData import USER_JSON

class USER_CLS:
    def __init__(self):
        self.file = USER_JSON
        with open(self.file, mode="r", encoding="utf-8") as f:
            self.dic = json.load(f)
    
    def load(self, ip:str) -> dict[str,str]:
        """読み込み"""
        if ip in self.dic:
            return self.dic[ip]
        else:
            return {}

    def update(self, ip:str, query:dict):
        """更新"""
        self.dic[ip] = query
    
    def clear(self, ip:str):
        if ip in self.dic:
            del self.dic[ip]
        self.dic[ip] = {}
        today = datetime.today()
        yesterday =  today - timedelta(days=1)
        self.dic[ip]["開始日付"] = yesterday.strftime(r"%Y-%m-%d")
        self.dic[ip]["終了日付"] = today.strftime(r"%Y-%m-%d")

    def refresh(self):
        """データ保存"""
        with open(self.file, mode="w", encoding="utf-8") as f:
            json.dump(self.dic, f, indent=2)

USER = USER_CLS()
