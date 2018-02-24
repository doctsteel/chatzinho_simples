"""Servidor para chat assincrono"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import random

clients = {}
addresses = {}

HOST = ''
PORT = 33000  # porta a ser usada
BUFSIZ = 1024 #tamanho maximo de cada mensagem
ADDR = (HOST, PORT) #endereao ip / porta
SERVER = socket(AF_INET, SOCK_STREAM)  #
SERVER.bind(ADDR)

def aceitar_conexoes():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s conectou" % client_address)

        addresses[client] = client_address
        Thread(target = entender_cliente, args = (client,)).start()

def entender_cliente(client): #pega o socket do cliente como argumento
    """gerencia a conexao de um cliente"""
    name = client.recv(BUFSIZ).decode("utf8")
    client.send(bytes("Conectado. \n", "utf8"))
    bemvindo = 'Nao zoe muito, essa merda esta um castelo de cartas'
    client.send(bytes(bemvindo+'\n', "utf8"))
    msg = "%s caiu de paraquedas na roda" % name
    broadcast(bytes(msg,"utf8"))
    clients[client] = name
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}","utf8"):
            broadcast(msg, name +">>> ")
        else:
            client.send(bytes("{quit}","utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s vazou do chat." % name, "utf8"))
            break

def broadcast(mensagem, prefixo = ""):
    """faz um broadcast pra todos os clientes. argumento prefixo e o nome da pessoa que enviou a mensagem"""
    for sock in clients:
        sock.send(bytes(prefixo, "utf8") + mensagem)

if __name__ == "__main__":
    SERVER.listen(50) #no maximo 5 pessoas no chat
    print("esperando conexao")
    ACCEPT_THREAD = Thread(target = aceitar_conexoes)
    ACCEPT_THREAD.start() # o main loop do servidor
    ACCEPT_THREAD.join()
    SERVER.close
