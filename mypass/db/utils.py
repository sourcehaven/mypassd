from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from mypass.crypto import checkpw
from mypass.exceptions import WrongPasswordException
from mypass.models.user import User
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
