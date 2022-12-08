from security.funciones_aes import iniciarAES_GCM, cifrarAES_GCM, descifrarAES_GCM


class Cipher:

    key = None
    o = None

    def __init__(self, key):
        self.key = bytes.fromhex(key)
        self.o = iniciarAES_GCM(self.key)

    def encrypt(self, strdata: str) -> dict:
        bstrdata = bytes(strdata, 'utf-8')
        datos_cifrado, mac_cifrado, aes_nonce = cifrarAES_GCM(self.o, bstrdata)

        return {
            'cipher_data': datos_cifrado.hex(),
            'mac': mac_cifrado.hex(),
            'nonce': aes_nonce.hex()
        }

    def decrypt(self, datos_cifrado: str, mac_cifrado: str, aes_nonce: str) -> str:
        return descifrarAES_GCM(self.key, aes_nonce, datos_cifrado, mac_cifrado)