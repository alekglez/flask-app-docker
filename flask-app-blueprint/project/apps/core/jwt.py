# -*- coding: utf-8 -*-

import time
import random
import jwt

from datetime import datetime, timedelta
from flask import current_app


class JWT:
    @staticmethod
    def encode(key, data):
        """
        Generate the authorization token.

        :param key: Key to use to generate the token
        :param data: Data to include within the token
        :return: The token
        """

        payload = {
            'exp': datetime.utcnow() + timedelta(seconds=current_app.config.get('JWT_LIFESPAN')),
            'jti': f'{time.time()}-{random.getrandbits(64)}',
            'iss': current_app.config.get('JWT_ISSUER'),
            'iat': datetime.utcnow(),
            'sub': data
        }

        try:
            return jwt.encode(payload, key=key, algorithm=current_app.config.get('JWT_ALGORITHM'))

        except jwt.exceptions.InvalidKeyError:
            JWTException('Invalid signature key!')

    @staticmethod
    def decode(key, token):
        """
        Validate the authorization token.

        :param key: Key to use to decode the token
        :param token: Token to validate
        :return:
        """

        try:
            payload = jwt.decode(token, key=key, algorithms=[current_app.config.get('JWT_ALGORITHM')])
            return payload['sub']

        except jwt.ExpiredSignatureError:
            raise JWTException('Token expired!')

        except jwt.InvalidTokenError:
            raise JWTException('Invalid token!')


class JWTException(Exception):
    """ JWT Exception """
    pass
