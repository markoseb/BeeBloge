from flask_security.utils import _security, _pwd_context, get_hmac
from werkzeug.security import check_password_hash


def verify_password(password, password_hash):
    """Returns ``True`` if the password matches the supplied hash.

    :param password: A plaintext password to verify
    :param password_hash: The expected hash value of the password (usually form your database)
    """
    if _security.password_hash != 'plaintext':
        password = get_hmac(password)

    return _pwd_context.verify(password, password_hash)