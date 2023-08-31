from datetime import datetime
from typing import Mapping

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
        user = db.session.query(User).filter_by(username=username).one()
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


def select_vault_entry(
        id: int = ...,
        user_id: int = ...,
        username: str = ...,
        title: str = ...,
        website: str = ...,
        notes: str = ...,
        folder: str = ...,
        create_time: datetime | str = ...,
        is_active: bool = ...
):
    crit = VaultEntry.map_criterion({
        'id': id, 'user_id': user_id, 'username': username, 'title': title, 'website': website,
        'notes': notes, 'folder': folder, 'create_time': create_time, 'is_active': is_active})
    return db.session.query(VaultEntry).filter_by(**crit).all()


def unlock_vault_entry(entry: VaultEntry | list[VaultEntry], enckey: str):
    try:
        for e in entry:
            e.encryptionkey = enckey
    except TypeError:
        entry.encryptionkey = enckey
    return entry


def update_vault_entry(
        user_id: int = ...,
        username: str = ...,
        title: str = ...,
        website: str = ...,
        notes: str = ...,
        folder: str = ...,
        create_time: datetime | str = ...,
        new_username: str = ...,
        new_title: str = ...,
        new_website: str = ...,
        new_notes: str = ...,
        new_folder: str = ...,
):
    if isinstance(create_time, str):
        create_time = datetime.fromisoformat(create_time)
    crit = VaultEntry.map_criterion({
        'user_id': user_id, 'username': username, 'title': title, 'website': website,
        'notes': notes, 'folder': folder, 'create_time': create_time})
    fields = VaultEntry.map_update({
        'username': new_username, 'title': new_title, 'website': new_website,
        'notes': new_notes, 'folder': new_folder})

    if len(fields) == 0:
        return 0

    entries = db.session.query(VaultEntry).filter_by(**crit).all()
    new_entries = [VaultEntry.copy(entry) for entry in entries]
    db.session.add_all(new_entries)
    # we need to get the ids of newly added items
    db.session.flush()
    affected_rows = 0
    for entry, new_entry in zip(entries, new_entries):
        affected_rows += db.session.query(VaultEntry).filter_by(id=entry.id).update(
            values={'is_active': False})
        affected_rows += db.session.query(VaultEntry).filter_by(id=new_entry.id).update(
            values={'parent_id': entry.id, **fields})

    db.session.commit()
    return affected_rows


def delete_vault_entry(crit: Mapping):
    if len(crit) > 0:
        db.session.query(VaultEntry).filter_by(**crit).delete()
        db.session.commit()
