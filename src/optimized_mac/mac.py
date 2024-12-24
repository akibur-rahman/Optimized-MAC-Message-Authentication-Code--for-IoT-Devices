import hashlib
from cryptography.hazmat.primitives import constant_time


class OptimizedMAC:
    def __init__(self, key, hash_function=hashlib.sha256):
        self.key = key if isinstance(key, bytes) else key.encode()
        self.hash_function = hash_function
        self.block_size = 64
        self.cache = {}
        self._precompute_keys()

    def _precompute_keys(self):
        if len(self.key) > self.block_size:
            self.key = self.hash_function(self.key).digest()
        padded_key = self.key.ljust(self.block_size, b'\x00')
        self.inner_key = bytes(x ^ 0x36 for x in padded_key)
        self.outer_key = bytes(x ^ 0x5c for x in padded_key)

    def generate(self, message):
        if not isinstance(message, bytes):
            message = message.encode()

        if message in self.cache:
            return self.cache[message]

        inner_hash = self.hash_function(self.inner_key + message).digest()
        mac = self.hash_function(self.outer_key + inner_hash).digest()

        self.cache[message] = mac
        return mac

    def verify(self, message, mac):
        return constant_time.bytes_eq(self.generate(message), mac)
