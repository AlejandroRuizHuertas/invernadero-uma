# import json
# from os import getenv
#
# from dotenv import load_dotenv
#
# from security.crypt import Cipher
#
# load_dotenv()
#
# data = {
#             'riego': 1,
#             'date': 2
#         }
#
# str_data = json.dumps(data, default=str)
#
# key = getenv("APP_KEY_INVERNADERO")
# cipher = Cipher(key)
# print(
#     cipher.encrypt(str_data)
# )
import json
from os import getenv

from dotenv import load_dotenv

from security.crypt import Cipher

bstr = b'{"cipher_data": "37ffca7bcec5860a7d17d7b9c9313931f2bad15b7f52649c49b4d2d55376a833aabb5daf2078c77089f00a1d70a5178f1cb99b8f56", "mac": "28453bc35b5ee1d59bf6976301b84ad2", "nonce": "b5fac5819b60c450d036f22ae8590c79"}'
str = bstr.decode('utf-8')
d = json.loads(str)
print(d)

load_dotenv()
key = getenv("APP_KEY_INVERNADERO")
cipher = Cipher(key)

print(cipher.decrypt(
    bytes.fromhex(d['cipher_data']),
    bytes.fromhex(d['mac']),
    bytes.fromhex(d['nonce'])
)
)