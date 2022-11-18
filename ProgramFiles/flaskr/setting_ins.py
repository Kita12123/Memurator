"""
設定情報
"""
import json

from ProgramData import SETTING_JSON

class SETTING_CLS:
    def __init__(self):
        self.file = SETTING_JSON
        try:
            with open(self.file, mode="r", encoding="utf-8") as f:
               self.dic = json.load(f)
        except(FileNotFoundError):
            self.dic = {
                    "最大表示行数":"",
                    "最終更新日時":""
                    }
            self.update()

    def update(self):
        """更新"""
        with open(self.file, mode="w", encoding="utf-8") as f:
            json.dump(self.dic, f, indent=2, ensure_ascii=False)

SETTING = SETTING_CLS()

