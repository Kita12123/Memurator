# .pycを作成しない
import sys
sys.dont_write_bytecode = True

import re

v = ",=4569 &>5944"

print(re.split("(?=[,|&])", v))

[
    "得意先コード >= 4429 AND 得意先コード <= 5500",
    "送荷先コード = 654192"
]
print(f"aaa{v:'*'^10}")