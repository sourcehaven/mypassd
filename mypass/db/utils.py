from mypass.models.user import User


def get_user_login(user, pw):
    """
    Fetches the user from the db only if username and password is correct.

    Parameters:
        user (str): Username to check against in the db.
        pw (str): Password for the username provided.
    Returns:
        (User | None): The user with the corresponding password if found,
        otherwise None.
    """

    raise NotImplementedError()
