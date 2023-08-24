from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from mypass.crypto import checkpw
from mypass.exceptions import WrongPasswordException
from mypass.models import User, VaultEntry, TokenBlacklist
from .db import db


def get_user_login(username, password):
    """
    Fetches the user from the db only if username and password is correct.

    Parameters:
        username (str): Username to check against in the db.
        password (str): Password for the username provided.

    Returns:
        (User): The user with the corresponding password if found,
        otherwise None.

    Raises:
        WrongPasswordException: If password does not match username.
    """

    try:
        user = db.session.query(User.create(username=username)).one()
        if checkpw(pw=password, salt=user.salt, hashedpw=user.hashedpassword):
            return user
    except (NoResultFound, MultipleResultsFound):
        pass
    raise WrongPasswordException('Could not found user with matching password.')


def is_blacklisted_token(token):
    return db.session.query(TokenBlacklist.token).filter_by(token=token).first() is not None


def insert_blacklist_token(jti: str):
    tbl = TokenBlacklist(token=jti)
    db.session.add(tbl)
    db.session.commit()
    return tbl


def insert_user(username: str, password: str, firstname: str = None, lastname: str = None, email: str = None):
    user = User.create(username=username, password=password, firstname=firstname, lastname=lastname, email=email)
    db.session.add(user)
    db.session.commit()
    return user


def insert_vault_entry(
        username: str = None,
        password: str = None,
        title: str = None,
        website: str = None,
        notes: str = None,
        folder: str = None
):
    entry = VaultEntry.create(
        username=username, password=password, title=title, website=website, notes=notes, folder=folder)
    db.session.add(entry)
    db.session.commit()
    return entry


def select_vault_entry():
    # TODO: implement select methods
    return db.session.query(VaultEntry).all()


def update_vault_entry():
    # TODO: implement update methods
    raise NotImplementedError()


def delete_vault_entry():
    # TODO: implement delete methods
    raise NotImplementedError()
