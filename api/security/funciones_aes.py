from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

def crear_AESKey():
    return get_random_bytes(16)


def iniciarAES_GCM(key_16):
    nonce_16 = get_random_bytes(16)
    aes_cifrado = AES.new(key_16, AES.MODE_GCM, nonce = nonce_16, mac_len = 16)
    return aes_cifrado

def cifrarAES_GCM(aes_cifrado, datos):
    datos_cifrado, mac_cifrado = aes_cifrado.encrypt_and_digest(datos)
    return datos_cifrado, mac_cifrado, aes_cifrado.nonce

def descifrarAES_GCM(key_16, nonce_16, datos, mac):
    try:
        aes_descifrado = AES.new(key_16, AES.MODE_GCM, nonce = nonce_16)
        datos_claro = aes_descifrado.decrypt_and_verify(datos, mac)
        return datos_claro
    except (ValueError, KeyError) as e:
        return False
        

def iniciarAES_CTR_cifrado(key_16):
    nonce_16_ini = get_random_bytes(8) # nonce aleatorio de 64 bits
                                       # --64 nonce--|--64 contador--
    ctr_16 = 0                         # contador, empezando desde 0
    aes_cifrado = AES.new(key_16, AES.MODE_CTR, nonce = nonce_16_ini, initial_value = ctr_16)
    return aes_cifrado, nonce_16_ini

def iniciarAES_CTR_descifrado(key_16, nonce_16_ini):
    ctr_16 = 0                      # contador, empezando desde 0. Origen y destino DEBEN tener este mismo valor
                                    # Si lees esto, piensa: ¿Que problema puede haber en que este valor sea siempre 0 en esta libreria?
    aes_descifrado = AES.new(key_16, AES.MODE_CTR, nonce = nonce_16_ini, initial_value = ctr_16)
    return aes_descifrado

def cifrarAES_CTR(aes_cifrado, datos):
    datos_cifrado = aes_cifrado.encrypt(datos)
    return datos_cifrado

def descifrarAES_CTR(aes_descifrado, datos):
    datos_claro = aes_descifrado.decrypt(datos)
    return datos_claro
