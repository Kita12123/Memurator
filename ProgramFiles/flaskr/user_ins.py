"""
ユーザー入力管理
"""
import json

from ProgramData import USER_JSON

class USER_CLS:
    def __init__(self):
        self.file = USER_JSON
        try:
            with open(self.file, mode="r", encoding="utf-8") as f:
                self.dic = json.load(f)
        except(FileNotFoundError):
            with open(self.file, mode="w", encoding="utf-8") as f:
                json.dump({}, f)
            self.dic = {}
    
    def load(self, ip:str) -> dict[str,str]:
        """読み込み"""
        if ip in self.dic:
            return self.dic[ip]
        else:
            return {}

    def update(self, ip:str, query:dict):
        """更新"""
        self.dic[ip] = query

    def refresh(self):
        """データ保存"""
        with open(self.file, mode="w", encoding="utf-8") as f:
            json.dump(self.dic, f, indent=2, ensure_ascii=False)

USER = USER_CLS()
