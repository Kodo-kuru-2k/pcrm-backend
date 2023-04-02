import os
from datetime import timedelta, datetime
from typing import Optional

import yagmail
import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class PasswordResetHandler:
    def __init__(self, user: str, password: str, secret_key: bytes):
        self.user = user
        self.password = password

        self.block_size = 16
        self.iv = os.urandom(self.block_size)
        self.secret_key = secret_key
        self.cipher = None

    def generate_random_string(self, emp_id: str) -> str:
        self.cipher = AES.new(self.secret_key, AES.MODE_CBC, self.iv)
        recovery_string = f"{emp_id}+{int((datetime.now() + timedelta(minutes=15)).timestamp())}".encode(
            "utf-8"
        )
        enc_recovery_string = self.cipher.encrypt(
            plaintext=pad(recovery_string, self.block_size)
        )
        return base64.urlsafe_b64encode(enc_recovery_string).decode("utf-8")

    def send_recovery_link(self, to: str, emp_id: str) -> None:
        recovery_string = self.generate_random_string(emp_id)
        recovery_link = f"http://localhost:5000/recovery-link/{recovery_string}"
        subject = "Password Recovery For Report Management System Login"
        content = [
            f""" here is the link for the recovery email <a href={recovery_link}> Link </a> 
                 This link is valid only for 15 min
            """
        ]
        with yagmail.SMTP(self.user, self.password) as yag:
            yag.send(to, subject, content)

    def decode_random_string(self, enc_recovery_string: str) -> Optional[str]:
        self.cipher = AES.new(self.secret_key, AES.MODE_CBC, self.iv)
        enc_recovery_string = base64.urlsafe_b64decode(
            enc_recovery_string.encode("utf-8")
        )
        recovery_string = unpad(
            self.cipher.decrypt(enc_recovery_string), self.block_size
        ).decode("utf-8")
        emp_id, time = recovery_string.split("+")
        if datetime.now().timestamp() >= int(time):
            return None
        return emp_id
