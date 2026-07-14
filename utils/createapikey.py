import secrets




def APIKEY(uid=None):
    api_key = secrets.token_hex(32)
    return api_key