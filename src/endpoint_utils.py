import logging
from flask import jsonify
from flask_jwt_extended import (create_access_token, 
create_refresh_token, set_access_cookies,
set_refresh_cookies)


def set_response_cookies(token_identity, resp=None, token_types=["access", "refresh"]):
    """
    Helper function to set cookies in response
    """
    logging.warning("Setting cookies")
    token_types.sort()
    if token_types == ["access", "refresh"]:
        access_token = create_access_token(identity = token_identity)
        refresh_token = create_refresh_token(identity = token_identity)
        if not resp:
            resp = jsonify({"access_token": access_token, "refresh_token": refresh_token})
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp 
    elif token_types == ["access"]:
        access_token = create_access_token(identity = token_identity)
        if not resp:
            resp = jsonify({"access_token": access_token})
        set_access_cookies(resp, access_token)
        return resp 
    elif token_types == ["refresh"]:
        refresh_token = create_refresh_token(identity = token_identity)
        if not resp:
            resp = jsonify({"refresh_token": refresh_token})
        set_refresh_cookies(resp, refresh_token)
        return resp 
    else:
        raise ValueError("Wrong Call to this function")