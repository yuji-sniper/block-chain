from ecdsa import SigningKey, NIST256p

class Wallet:
    def __init__(self):
        self._private_key = SigningKey.generate(curve=NIST256p)
        self._public_key = self._private_key.get_verifying_key()
    
    @property
    def private_key(self):
        return self._private_key.to_string().hex()
    
    @property
    def public_key(self):
        return self._public_key.to_string().hex()

    def sign(self, data):
        return self._private_key.sign(data)

    def verify(self, signature, data):
        return self._public_key.verify(signature, data)


if __name__ == '__main__':
    wallet = Wallet()
    print(wallet.private_key)
    print(wallet.public_key)
