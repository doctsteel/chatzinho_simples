import connexion
import six

from swagger_server.models.msg import Msg  # noqa: E501
from swagger_server.models.sent_msg import SentMsg  # noqa: E501
from swagger_server import util


def broadcast_post(mensagem):  # noqa: E501
    """popula o chat

    popula o chat # noqa: E501

    :param mensagem: 
    :type mensagem: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        mensagem = Msg.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def join_user_get(user):  # noqa: E501
    """Junta usuário novo ao servidor

    Salva o nome no banco de dados do usuário dentro do chat # noqa: E501

    :param user: nome do usuario
    :type user: str

    :rtype: None
    """
    return 'do some magic!'


def quit_user_get(user):  # noqa: E501
    """desconecta o user do server

    deleta o nome no banco de dados do usuário dentro do chat # noqa: E501

    :param user: nome do usuario
    :type user: str

    :rtype: None
    """
    return 'do some magic!'


def receive_post(message):  # noqa: E501
    """recebe mensagem do cliente

    ficar digitando duas vezes a mesma coisa é ruim # noqa: E501

    :param message: a mensagem no corpo da requisição a ser publicada
    :type message: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        message = SentMsg.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
