from Crypto.Hash import SHA256


class PasswordHash:
    @staticmethod
    def hash_password(password: str):
        h = SHA256.new()
        h.update(password.encode("utf-8"))
        return h.hexdigest()

    @staticmethod
    def compare_hash(password: str, hashed_password: str):
        h = SHA256.new()
        h.update(password.encode("utf-8"))
        if h.hexdigest() == hashed_password:
            return True
        return False
