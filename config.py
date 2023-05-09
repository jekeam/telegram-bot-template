API_KEY = "Yout API KEY form https://t.me/BotFather"
LOG_LEVEL = "DEBUG"
ADMINS = [
    # Our Admin IDs
    381868674,  # My
]
DEFAULT_LANG = 'ru'
DB_USER_STATUS_OFF = "off"

with open("lang.json", "r", encoding="utf8") as f:
    import json

    # lang_code see https://en.wikipedia.org/wiki/IETF_language_tag
    LANG = json.load(f)
