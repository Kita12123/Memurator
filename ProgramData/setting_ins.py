"""
設定情報
"""
import os
import json

class SETTING_CLS:
    def __init__(self):
        self.file = os.path.join(
            os.path.dirname(__file__),
            "setting.json")
        with open(self.file, mode="r", encoding="cp932") as f:
            self.dic = json.load(f)

    def update(self):
        """更新"""
        with open(self.file, mode="w", encoding="cp932") as f:
            json.dump(self.dic, f)

SETTING = SETTING_CLS()