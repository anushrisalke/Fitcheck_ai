import jwt

SECRET_KEY = "fitcheck_secret_key"


def create_access_token(email):
    token = jwt.encode(
        {
            "email": email
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return token


def verify_token(token):
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=["HS256"]
    )

    return payload