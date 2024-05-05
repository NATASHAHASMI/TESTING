import os

ENVIRONMENT = os.environ.get('ENVIRONMENT', False)

if ENVIRONMENT:
    try:
        API_ID = int(os.environ.get('API_ID', 0))
    except ValueError:
        raise Exception("Your API_ID is not a valid integer.")
    API_HASH = os.environ.get('API_HASH', None)
    BOT_TOKEN = os.environ.get('BOT_TOKEN', None)
    DATABASE_URL = os.environ.get('DATABASE_URL', None)
    DATABASE_URL = DATABASE_URL.replace("postgres", "postgresql")  # Sqlalchemy dropped support for "postgres" name.
    # https://stackoverflow.com/questions/62688256/sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy-dialectspostgre
    MUST_JOIN = os.environ.get('MUST_JOIN', None)
    if MUST_JOIN.startswith("@"):
        MUST_JOIN = MUST_JOIN.replace("@", "")
else:
    # Fill the Values
    API_ID = 22427221
    API_HASH = "2785b4528c12682e515db3762463c126"
    BOT_TOKEN = "6550852346:AAHN6R9CGY0lL8RN2SF-VP9aohp6vVXVS6M"
    DATABASE_URL = "postgres://koyeb-adm:7yEXzg3wFtZK@ep-yellow-math-a2ziaq6n.eu-central-1.pg.koyeb.app/koyebdb"
    DATABASE_URL = DATABASE_URL.replace("postgres", "postgresql")
    MUST_JOIN = "MYFLiiX"
    if MUST_JOIN.startswith("@"):
        MUST_JOIN = MUST_JOIN[1:]
