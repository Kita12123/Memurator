from flaskr.common.model import Session
from flaskr.common.model.user import User

def user_load(id: str, /) -> dict[str, str | int]:
    with Session() as session, session.begin():
        user = session.query(User).filter(
            User.id==id
        ).one_or_none()
        if user is None:
            user = User(id=id)
            session.add(user)
            session.commit()
        user_dic = user.to_dict()
    return user_dic
