from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData

from ProgramData import PROGRAM_DIR

db_path = PROGRAM_DIR / "database.db"

engine = create_engine(
    f"sqlite:///{db_path}",
    echo=True
)

meta = MetaData(engine)

Base = declarative_base(metadata=meta)

Session = sessionmaker(
    autocommit=False,
    # session.commit()するまでは実行されない
    autoflush=False,
    bind=engine
)


# データベース作成
from flaskr.common.model import database
from flaskr.common.model import user

Base.metadata.create_all(engine)
