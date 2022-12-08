from datetime import datetime, timedelta
from os import getenv
from jwt import encode


def __expire_date(days: int) -> datetime:
    now = datetime.now()
    return now + timedelta(days)

#TODO: Esto no me gusta aqui
def set_token(user):
    secret = getenv("APP_KEY")
    algorithm = getenv("APP_ALGORITHM")

    user["token"] = encode(
        {
            "user_id": user["_id"],
            "exp": __expire_date(1)
        },
        secret,
        algorithm=algorithm
    )

    return user