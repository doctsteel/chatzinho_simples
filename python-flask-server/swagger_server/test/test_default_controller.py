# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.msg import Msg  # noqa: E501
from swagger_server.models.sent_msg import SentMsg  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_broadcast_post(self):
        """Test case for broadcast_post

        popula o chat
        """
        mensagem = Msg()
        response = self.client.open(
            '/v2/broadcast',
            method='POST',
            data=json.dumps(mensagem),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_join_user_get(self):
        """Test case for join_user_get

        Junta usuário novo ao servidor
        """
        response = self.client.open(
            '/v2/join/{user}'.format(user='user_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_quit_user_get(self):
        """Test case for quit_user_get

        desconecta o user do server
        """
        response = self.client.open(
            '/v2/quit/{user}'.format(user='user_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_receive_post(self):
        """Test case for receive_post

        recebe mensagem do cliente
        """
        message = SentMsg()
        response = self.client.open(
            '/v2/receive',
            method='POST',
            data=json.dumps(message),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
