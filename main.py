import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import *
import socket
from kivy.clock import Clock

HOST = '177.95.244.227' #IP A SER CONECTADO
PORT = 33000            #PORTA A SE CONECTAR NO HOST

BUFSIZ = 1024           #pra referencia qual o tamanho MÁXIMO de dados que vai ser enviado e recebido
ADDR = (HOST, PORT)     #a ser usado com o método connect da biblioteca socket do python

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #ainda preciso entender HUE
client_socket.connect(ADDR)                   #é isso
client_socket.setblocking(0)
                      #começa a thread


def receber(objeto):
    try:
        mail = client_socket.recv(BUFSIZ).decode("utf8")
        objeto.chatoutput.insert_text(mail+ "\n")
    except (OSError, socket.error):
        pass
def update(objeto):
    receber(objeto)

class FloatWidget(FloatLayout):
    chatoutput = ObjectProperty()
    chatinput = ObjectProperty()
    buttonsend = ObjectProperty()
    boxbaixo = BoxLayout()
    active = 0
    def sendMessage(self):
        mensagem = self.boxbaixo.chatinput.text
        self.boxbaixo.chatinput.text = ""
        client_socket.send(mensagem.encode("utf8"))
        if self.active == 0:
            Clock.schedule_interval(lambda dt:update(self), 1)
            self.active = 1
        if mensagem =="{quit}":
            client_socket.close()
            ChatApp.stop()



class ChatApp(App):

    def build(self):
        return FloatWidget()




if __name__ == '__main__':
    ChatApp().run()
