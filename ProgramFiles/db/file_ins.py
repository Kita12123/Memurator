"""
ファイル定義インスタンス作成
"""
from ProgramFiles.db.mod import HostFileDefine

INS_LIST: list[HostFileDefine] = []

#
# Instance
#

#
# 営業
#

MUJNRPF_MOLIB = HostFileDefine(
    file_name="MUJNRPF",
    lib_name="MOLIB",
    columns_dic={
        "伝票日付": ("DYMD", "INTEGER"),
        "得意先コード": ("TOKCD", "INTEGER"),
        "得意先カナ": ("TOKNM", "TEXT"),
        "雑コード": ("ZATUCD", "INTEGER"),
        "伝票区分": ("DENK", "INTEGER"),
        "委託区分": ("ITAK", "INTEGER"),
        "扱い運送": ("ATU", "INTEGER"),
        "担当者コード": ("TANCD", "INTEGER"),
        "送荷先コード": ("ATUNM", "INTEGER"),
        "送荷先カナ": ("SOK", "TEXT"),
        "製品部品コード": ("CODE", "INTEGER"),
        "製品部品カナ": ("HINNM", "TEXT"),
        "級区分": ("KKBN", "INTEGER"),
        "数量": ("SUR", "INTEGER"),
        "単価": ("TANKA", "INTEGER"),
        "原価": ("TANATA", "REAL"),
        "金額": ("KIN", "INTEGER"),
        "出荷伝票番号": ("SDENNO", "TEXT"),
        "オーダー番号": ("ODER", "TEXT"),
        "備考": ("BIKO", "TEXT"),
        "ブロック番号": ("BLK", "INTEGER"),
        "ブロック行": ("GYO", "INTEGER")
        }
)
INS_LIST.append(MUJNRPF_MOLIB)

UJNRPFW_FLIB1 = HostFileDefine(
    file_name="UJNRPFW",
    lib_name="FLIB1",
    columns_dic={
        "伝票日付": ("DENYMD", "INTEGER"),
        "得意先コード": ("TOKCD", "INTEGER"),
        "得意先カナ": ("TOKMEK", "TEXT"),
        "雑コード": ("ZATUCD", "INTEGER"),
        "伝票区分": ("DENKBN", "INTEGER"),
        "委託区分": ("ITACD", "INTEGER"),
        "扱い区分": ("ATUKAI", "INTEGER"),
        "運送会社コード": ("UNSOCD", "INTEGER"),
        "担当者コード": ("TANCD", "INTEGER"),
        "送荷先コード": ("ATUMEI", "INTEGER"),
        "送荷先カナ": ("SOKMEI", "TEXT"),
        "製品部品コード": ("SEIBUC", "INTEGER"),
        "製品部品カナ": ("HINMEI", "TEXT"),
        "級区分": ("KYUKBN", "INTEGER"),
        "数量": ("SURYO", "INTEGER"),
        "単価": ("TANKA", "INTEGER"),
        "出荷伝票番号": ("SYUDEN", "TEXT"),
        "オーダー番号": ("ODER", "TEXT"),
        "備考": ("BIKO", "TEXT"),
        "ブロック番号": ("BLKNO", "INTEGER"),
        "ブロック行": ("GYONO", "INTEGER")
    }
)
INS_LIST.append(UJNRPFW_FLIB1)

UJNRPF_FLIB1 = HostFileDefine(
    file_name="UJNRPF",
    lib_name="FLIB1",
    columns_dic={
        "伝票日付": ("DENYMD", "INTEGER"),
        "得意先コード": ("TOKCD", "INTEGER"),
        "得意先カナ": ("TOKMEK", "TEXT"),
        "雑コード": ("ZATUCD", "INTEGER"),
        "伝票区分": ("DENKBN", "INTEGER"),
        "委託区分": ("ITACD", "INTEGER"),
        "扱い区分": ("ATUKAI", "INTEGER"),
        "運送会社コード": ("UNSOCD", "INTEGER"),
        "担当者コード": ("TANCD", "INTEGER"),
        "送荷先コード": ("ATUMEI", "INTEGER"),
        "送荷先カナ": ("SOKMEI", "TEXT"),
        "製品部品コード": ("SEIBUC", "INTEGER"),
        "製品部品カナ": ("HINMEI", "TEXT"),
        "級区分": ("KYUKBN", "INTEGER"),
        "数量": ("SURYO", "INTEGER"),
        "単価": ("TANKA", "INTEGER"),
        "出荷伝票番号": ("SYUDEN", "TEXT"),
        "オーダー番号": ("ODER", "TEXT"),
        "備考": ("BIKO", "TEXT"),
        "ブロック番号": ("BLKNO", "INTEGER"),
        "ブロック行": ("GYONO", "INTEGER")
    }
)
INS_LIST.append(UJNRPF_FLIB1)

SYUKAPF_FLIB = HostFileDefine(
    file_name="SYUKAPF",
    lib_name="FLIB",
    columns_dic={
        "伝票日付": ("S08", "INTEGER"),
        "指示日付": ("S07", "INTEGER"),
        "出荷伝票番号": ("S03", "TEXT"),
        "出荷行番号": ("S04", "INTEGER"),
        "伝票区分": ("S09", "INTEGER"),
        "委託区分": ("S10", "INTEGER"),
        "得意先コード": ("S12", "INTEGER"),
        "得意先カナ": ("S13", "TEXT"),
        "雑コード": ("ZATUCD", "INTEGER"),
        "担当者コード": ("S199", "INTEGER"),
        "送荷先コード": ("S20", "INTEGER"),
        "送荷先カナ": ("S36", "TEXT"),
        "扱い運送": ("S21", "INTEGER"),
        "製品部品コード": ("S25", "INTEGER"),
        "製品部品カナ": ("S27", "TEXT"),
        "級区分": ("S24", "INTEGER"),
        "部番": ("S26", "TEXT"),
        "受注数": ("S29", "INTEGER"),
        "出荷数": ("S30", "INTEGER"),
        "売上数": ("S31", "INTEGER"),
        "ＢＯ区分": ("S31", "INTEGER"),
        "単価": ("S33", "INTEGER"),
        "金額": ("S34", "INTEGER"),
        "オーダー番号": ("S28", "TEXT"),
        "備考": ("S35", "TEXT"),
        "入力日": ("HONJIT", "INTEGER"),
        "入力時": ("HH", "INTEGER"),
        "入力分": ("MM", "INTEGER")
    }
)
INS_LIST.append(SYUKAPF_FLIB)

ETCMPF_FLIB = HostFileDefine(
    file_name="ETCMPF",
    lib_name="FLIB",
    columns_dic={
        "レコード区分＊": ("RKBN", "INTEGER"),
        "コード＊": ("CODE", "INTEGER"),
        "名称＊": ("NAME", "TEXT"),
        "カナ＊": ("NAME2", "TEXT"),
        "数値＊": ("SUU", "INTEGER")
    }
)
INS_LIST.append(ETCMPF_FLIB)

NIHONPF_FLIB = HostFileDefine(
    file_name="NIHONPF",
    lib_name="FLIB",
    columns_dic={
        "送荷先コード＊": ("コード", "INTEGER"),
        "送荷先カナ＊": ("日本語１カナ", "TEXT"),
        "送荷先名＊": ("日本語１漢字", "TEXT"),
        "県コード＊": ("県コード", "INTEGER"),
        "電話番号＊": ("電話番号", "TEXT"),
        "郵便番号１＊": ("郵便番号１", "INTEGER"),
        "郵便番号２＊": ("郵便番号２", "INTEGER"),
        "住所１＊": ("日本語２漢字", "TEXT"),
        "住所２＊": ("日本語３漢字", "TEXT")
    }
)
INS_LIST.append(NIHONPF_FLIB)

TOKMPF_FLIB = HostFileDefine(
    file_name="TOKMPF",
    lib_name="FLIB",
    columns_dic={
        "得意先コード１＊": ("TOKCD1", "INTEGER"),
        "得意先コード２＊": ("TOKCD2", "INTEGER"),
        "得意先カナ＊": ("TOKA1", "TEXT"),
        "得意先名＊": ("TOKJ1", "TEXT"),
        "担当者コード＊": ("TANCD", "INTEGER"),
        "県コード＊": ("KENCD", "INTEGER"),
        "郵便番号１＊": ("YUBIA1", "INTEGER"),
        "郵便番号２＊": ("YUBIA2", "INTEGER"),
        "住所１＊": ("ADLJ1", "TEXT"),
        "住所２＊": ("ADLJ2", "TEXT"),
        "電話番号＊": ("TELNO", "TEXT"),
        "作成日＊": ("SAKUSE", "INTEGER"),
        "締め日＊": ("SIMEBI", "INTEGER"),
        "ＬＥＳＳ率＊": ("LESS", "INTEGER")
    }
)
INS_LIST.append(TOKMPF_FLIB)

KENPF_FLIB1 = HostFileDefine(
    file_name="KENPF",
    lib_name="FLIB1",
    columns_dic={
        "県コード＊": ("CODE", "INTEGER"),
        "県名＊": ("NAME", "TEXT")
    }
)
INS_LIST.append(KENPF_FLIB1)

SEIMPF_FLIB = HostFileDefine(
    file_name="SEIMPF",
    lib_name="FLIB",
    columns_dic={
        "製品コード＊": ("機種コード", "INTEGER"),
        "製品カナ＊": ("製品名", "TEXT"),
        "分類＊": ("製品分類", "INTEGER"),
        "集計コード＊": ("集計用ＣＤ", "INTEGER"),
        "１級単価＊": ("１級売単価", "INTEGER"),
        "１級原価＊": ("１級原価", "INTEGER"),
        "２級単価＊": ("２級売単価", "INTEGER"),
        "２級原価＊": ("２級原価", "INTEGER"),
        "廃止区分＊": ("重点品目区分", "TEXT"),
        "作成日＊": ("作成日", "INTEGER"),
        "税率区分＊": ("SEKBN", "INTEGER"),
        "重量＊": ("重量㎏", "REAL")
    }
)
INS_LIST.append(SEIMPF_FLIB)

BUHMPF_FLIB = HostFileDefine(
    file_name="BUHMPF",
    lib_name="FLIB",
    columns_dic={
        "部品コード＊": ("RKEY", "INTEGER"),
        "部品カナ＊": ("NAME", "TEXT"),
        "部番＊": ("BAN", "TEXT"),
        "単価＊": ("TANK1", "REAL"),
        "原価＊": ("TANK2", "REAL"),
        "旧単価＊": ("TANKS", "REAL"),
        "代替区分＊": ("DAIK", "INTEGER"),
        "代替コード＊": ("DAIC", "INTEGER"),
        "重量＊": ("JURYO", "REAL"),
        "廃止区分＊": ("HAISIF", "INTEGER"),
        "作成日＊": ("CRTYMD", "INTEGER")
    }
)
INS_LIST.append(BUHMPF_FLIB)

#
# 工場
#

NSFILEP_MOLIB = HostFileDefine(
    file_name="NSFILEP",
    lib_name="MOLIB",
    columns_dic={
        "伝票日付": ("DYMD", "INTEGER"),
        "納期": ("NOUKI", "INTEGER"),
        "手配先コード": ("SIR", "INTEGER"),
        "手配先カナ": ("SIRNM", "TEXT"),
        "補用区分": ("HOYOKB", "TEXT"),
        "品目コード": ("BUCD", "TEXT"),
        "品目カナ": ("BUHNM", "TEXT"),
        "数量": ("SUR", "INTEGER"),
        "単価": ("TANKA", "REAL"),
        "金額": ("KIN", "INTEGER"),
        "機種コード": ("KIS", "TEXT"),
        "機種カナ": ("KISNM", "TEXT"),
        "勘定科目カナ１": ("KAMOK1", "TEXT"),
        "勘定科目カナ２": ("KAMOK2", "TEXT"),
        "注文番号": ("CHU", "TEXT")
    }
)
INS_LIST.append(NSFILEP_MOLIB)

RIPPET_FLIB = HostFileDefine(
    file_name="RIPPET",
    lib_name="FLIB",
    columns_dic={
        "レコード区分＊": ("データ区分", "INTEGER"),
        "コード＊": ("コード", "INTEGER"),
        "カナ＊": ("カナ名称", "TEXT"),
        "名称＊": ("名称", "TEXT"),
        "数値１＊": ("数値", "REAL"),
        "数値２＊": ("数値（２）", "REAL")
    }
)
INS_LIST.append(RIPPET_FLIB)

RIPPTR_FLIB = HostFileDefine(
    file_name="RIPPTR",
    lib_name="FLIB",
    columns_dic={
        "手配先コード＊": ("コード", "INTEGER"),
        "手配先名＊": ("仕入先名", "TEXT"),
        "手配先略称＊": ("仕入先名（略称）", "TEXT")
    }
)
INS_LIST.append(RIPPTR_FLIB)

PMDBPF_FLIB = HostFileDefine(
    file_name="PMDBPF",
    lib_name="FLIB",
    columns_dic={
        "品目コード＊": ("DBCTRL", "TEXT"),
        "品目分類＊": ("HSMALL", "INTEGER"),
        "品目カナ＊": ("HINMEI", "TEXT"),
        "品目名＊": ("HINMEN", "TEXT"),
        "仕様＊": ("SIYOU", "TEXT"),
        "図番＊": ("ZUBAN", "TEXT"),
        "部番＊": ("BUBAN", "TEXT"),
        "手配先コード＊": ("TEHAI", "INTEGER"),
        "納入先コード＊": ("NOUNYU", "INTEGER"),
        "資材単価＊": ("ASHI", "REAL"),
        "加工単価＊": ("AKAK", "REAL"),
        "検査区分＊": ("KENKBN", "INTEGER"),
        "作成日＊": ("CRTYMD", "INTEGER"),
        "変更日＊": ("UPDYMD", "INTEGER")
    }
)
INS_LIST.append(PMDBPF_FLIB)

TEHAIPF_KITAURA = HostFileDefine(
    file_name="TEHAIPF",
    lib_name="KITAURA",
    columns_dic={
        "手配先コード": ("手配先コード", "INTEGER"),
        "手配先名": ("手配先名", "TEXT"),
        "発注日": ("発注日", "INTEGER"),
        "納期": ("納期", "INTEGER"),
        "品目コード": ("品目コード", "TEXT"),
        "品目カナ": ("品目カナ", "TEXT"),
        "品目名": ("品目名", "TEXT"),
        "仕様": ("仕様", "TEXT"),
        "図番": ("図番", "TEXT"),
        "材料単価": ("材料単価", "REAL"),
        "加工単価": ("加工単価", "REAL"),
        "数量": ("数量", "REAL"),
        "納品書番号": ("納品書ＮＯ", "INTEGER"),
        "注文番号": ("注文ＮＯ", "TEXT"),
        "納入先コード": ("納入先コード", "INTEGER"),
        "納入場所": ("納入場所", "TEXT"),
        "注文区分": ("注文区分", "TEXT"),
        "発注区分": ("発注区分", "TEXT"),
        "検査区分": ("検査区分", "TEXT"),
        "親コード": ("親コード", "TEXT"),
        "親カナ": ("親カナ", "TEXT"),
        "親納期": ("親納期", "INTEGER"),
        "機種１": ("機種１", "TEXT"),
        "原単位１": ("原単位１", "REAL"),
        "発注日１": ("発注日１", "INTEGER"),
        "不良内容１": ("不良内容１", "TEXT"),
        "機種２": ("機種２", "TEXT"),
        "原単位２": ("原単位２", "REAL"),
        "発注日２": ("発注日２", "INTEGER"),
        "不良内容２": ("不良内容２", "TEXT"),
        "機種３": ("機種３", "TEXT"),
        "原単位３": ("原単位３", "REAL"),
        "発注日３": ("発注日３", "INTEGER"),
        "不良内容３": ("不良内容３", "TEXT"),
        "機種４": ("機種４", "TEXT"),
        "原単位４": ("原単位４", "REAL"),
        "発注日４": ("発注日４", "INTEGER"),
        "不良内容４": ("不良内容４", "TEXT"),
        "機種５": ("機種５", "TEXT"),
        "原単位５": ("原単位５", "REAL"),
        "発注日５": ("発注日５", "INTEGER"),
        "不良内容５": ("不良内容５", "TEXT"),
    }
)
INS_LIST.append(TEHAIPF_KITAURA)
