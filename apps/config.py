from pathlib import Path

basedir = Path(__file__).parent.parent


class BaseConfig:
    SECRET_KEY = "grjeotjowTR$WVO49trewsJ"
    # スケジュール設定
    SCHEDULER_API_ENABLED = True
    # デバッグツールバー
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'testing.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


# config辞書にマッピングする
config = {
    "testing": TestingConfig,
    "local": LocalConfig,
}