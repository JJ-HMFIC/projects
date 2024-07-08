import time

import bcrypt
import random
from jose import jwt
from datetime import datetime, timedelta


class UserService:
    encoding: str = "UTF-8"
    secret_key: str = "0d376ca09fce3ae19a2e6e2ced5fe9d396dec065b7a48ec22bcfbc0ac47dd820"
    jwt_algorithm = "HS256"

    def hash_password(self, plain_password: str) -> str:
        hash: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding), salt=bcrypt.gensalt())
        return hash.decode(self.encoding)

    def verify_password(self,
                        plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding)
        )

    def create_jwt(self, username: dict) -> str:
        return jwt.encode(
            {
                "sub": username,  # 유저 식별자, unique id
                "exp": datetime.now() + timedelta(days=1)  # 토큰의 만료시간 = 하루
            },
            self.secret_key,
            algorithm=self.jwt_algorithm)

    def decode_jwt(self, access_token: str) -> str:
        payload: dict = jwt.decode(
            access_token, self.secret_key, algorithms=[self.jwt_algorithm]
        )
        # expire
        return payload["sub"]  # username

    @staticmethod
    def create_otp() -> int:
        return random.randint(1000, 9999)

    @staticmethod
    def send_email_to_user(email: str) -> None:
        time.sleep(10)
        print(f"Sending email to {email}!")
