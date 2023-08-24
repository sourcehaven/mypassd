import os

from flask_jwt_extended import get_jwt_identity

from mypass.models import User, VaultEntry
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

if __name__ == '__main__':
    identity = get_jwt_identity()

    engine = create_engine(os.environ['MYPASS_DB_CONNECTION_URI'], echo=True)
    user = User.create(username='whodahell', password='--**--||--**--')
    vaultentry = VaultEntry(uid=2, username='mypass', password='PassWORD')

    # with Session(bind=engine) as session:
    #     session.add(user)
    #     session.commit()

    # with Session(bind=engine) as session:
    #     session.add(vaultentry)
    #     session.commit()

    with Session(bind=engine) as session:
        user_select = list(session.query(User))

    with Session(bind=engine) as session:
        vault_select = list(session.query(VaultEntry))

    print('Finished ...')
