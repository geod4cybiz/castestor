from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin
from itsdangerous import URLSafeTimedSerializer, BadSignature

from time import time
# import jwt
import hashlib
import uuid

from app import app,cache

def gen_ticket(user,service,timeout=60):
    exp = int(time()) + timeout
    ts = int(time()) + 10

    data = { 'userid':user.id , 'service': service ,'exp': exp}

    m = hashlib.sha256()
    m.update((app.config['CACHE_KEY_PREFIX'] + str(uuid.uuid4())).encode())
    cachekey=m.hexdigest()
    cache.set(cachekey,data,timeout = (ts + timeout))

    return f'ST_{cachekey}'

def decode_ticket(ticket):
    data = cache.get(ticket.replace('ST_',''))
    return data


