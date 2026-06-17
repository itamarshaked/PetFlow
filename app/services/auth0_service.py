import json
from functools import wraps
from urllib.request import urlopen

from flask import request, jsonify, current_app, g
from jose import jwt


def get_token_auth_header():
    auth = request.headers.get("Authorization", None)

    if not auth:
        return None, ("authorization header is expected", 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        return None, ("authorization header must start with Bearer", 401)

    if len(parts) == 1:
        return None, ("token not found", 401)

    if len(parts) > 2:
        return None, ("authorization header must be Bearer token", 401)

    return parts[1], None

def verify_auth0_token(token):
    auth0_domain = current_app.config.get("AUTH0_DOMAIN")
    audience = current_app.config.get("AUTH0_AUDIENCE")
    issuer = current_app.config.get("AUTH0_ISSUER")

    jwks_url = f"https://{auth0_domain}/.well-known/jwks.json"
    jsonurl = urlopen(jwks_url)
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }

    if not rsa_key:
        raise Exception("Unable to find appropriate key")

    payload = jwt.decode(
        token,
        rsa_key,
        algorithms=["RS256"],
        audience=audience,
        issuer=issuer,
    )

    return payload

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token, error = get_token_auth_header()

        if error:
            message, status = error
            return jsonify({"error": message}), status

        try:
            payload = verify_auth0_token(token)
        except Exception as exc:
            return jsonify(
                {
                    "error": "invalid token",
                    "details": str(exc)
                }
            ), 401

        g.auth0_user = payload

        return f(*args, **kwargs)

    return decorated