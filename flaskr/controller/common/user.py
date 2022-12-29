from flaskr.model import Session
from flaskr.model.user import User


def load_user(id: str) -> User:
    """ユーザー読み込み（新規なら作成する）"""
    with Session() as session, session.begin():
        user = session.query(User).filter_by(
            id=id
        ).one_or_none()
        if user is None:
            user = User(id=id)
            session.add(user)
            session.commit()
    return user
