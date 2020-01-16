# -*- coding: utf-8 -*-

from unittest import TestCase
from ..jwt import JWT


class TestJWT(TestCase):
    def test_code_decode_jwt_token(self):
        data, key = {'key': 'some_value'}, 'some_secret_key'
        token = JWT.encode(key, data)
        self.assertTrue(isinstance(token, bytes))

        payload = JWT.decode(key, token)
        self.assertEqual(data, payload)
