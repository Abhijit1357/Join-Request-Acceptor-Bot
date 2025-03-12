from os import environ

API_ID = int(environ.get("API_ID", "22834593"))
API_HASH = environ.get("API_HASH", "f400bc1d1baeb9ae93014ce3ee5ea835")
BOT_TOKEN = environ.get("BOT_TOKEN", "7729465278:AAF_Ao-SfzIleZiiENbkx32uv7UPCTGOXc4")
#Make Bot Admin In Log Channel With Full Rights
LOG_CHANNEL = int(environ.get("LOG_CHANNEL", "-1002134425165"))
ADMINS = int(environ.get("ADMINS", "6148346742"))
#Warning - Give Db uri in deploy server environment variable, don't give in repo.
DB_URI = environ.get("DB_URI", "mongodb+srv://AOMusic:AOMusic@cluster0.sibxiqk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
#Warning - Give Db uri in deploy server environment variable, don't give in repo.
DB_NAME = environ.get("DB_NAME", "vjjoinrequetbot")
#If this is True Then Bot Accept New Join Request
NEW_REQ_MODE = bool(environ.get('NEW_REQ_MODE', False))
LOG_TEXT = "Koi message aaya hai!\n\nUser ID: {}\nUser Mention: {}"
