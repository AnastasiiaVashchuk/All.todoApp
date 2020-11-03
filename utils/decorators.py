from functools import wraps
from flask import redirect, session


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get('username', None):
            return f(*args, **kwargs)
        else:
            return redirect('/login/')
    return wrap
