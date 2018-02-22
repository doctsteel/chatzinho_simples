from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from kivy.properties import *

HOST = 'localhost' #IP A SER CONECTADO
PORT = 33000            #PORTA A SE CONECTAR NO HOST

BUFSIZ = 1024           #pra referencia qual o tamanho MÁXIMO de dados que vai ser enviado e recebido
ADDR = (HOST, PORT)     #a ser usado com o método connect da biblioteca socket do python

client_socket = socket(AF_INET, SOCK_STREAM)  #ainda preciso entender HUE
client_socket.connect(ADDR)                   #é isso

                      #começa a thread




class ReceiveName(FloatLayout):
    def __init__(self, **kwargs):
        super(ReceiveName, self).__init__(**kwargs)
        self.add_widget(Label(text = "seu nome, por favor", size_hint=(0.3, 0.02), pos_hint={'center_x':0.5, 'center_y':0.4}))
        self.lacunanome = TextInput(background_color = [0, 0, 0, 1],text=">>", foreground_color = [1, 1, 1, 1], multiline = False, size_hint=(0.3, 0.04), pos_hint={'center_x':0.5, 'center_y':0.36}, font_size= 12)
        self.add_widget(self.lacunanome)
        self.btn = Button(text="eh isto!", size_hint=(0.3, 0.07), pos_hint={'center_x':0.5, 'center_y':0.28})
        self.btn.bind(on_press=self.callback)
        self.add_widget(self.btn)
        receive_thread = Thread(target=self.receber)        #cria uma thread de loop infinito do método receber(), pra ficar esperando e recebendo coisa nova do chat
        receive_thread.start()
        self.mainchatscreen = TextInput(readonly = True, background_color = [0, 0, 0, 1], foreground_color = [1, 1, 1, 1], multiline = True, size_hint=(0.9, 0.7), pos_hint={'center_x':0.1, 'center_y':0.9}, font_size= 15)
        self.messagechat = TextInput(background_color = [30, 30, 30, 1], multiline = False, size_hint = (0.3, 0.04), pos_hint = {'center_x':0.4, 'center_y':0.1 })
        self.sendbutton = Button(text = "enviar", size_hint=(0.25, 0.07), pos_hint={'center_x':0.75, 'center_y':0.1})
        self.sendbutton.bind(on_press = self.sendMessage)

    def callback(self,nutton):
        client_socket.send(bytes(self.lacunanome.text,"utf8"))
        self.lame = self.lacunanome.text
        self.createChatBox()

    def createChatBox(self):
        self.clear_widgets()
        self.nomedeusuario = Label(text = self.lame +" ---->>", pos_hint={'center_x':0.05, 'center_y':0.1}, size_hint=(0.3, 0.02))

        self.add_widget(self.nomedeusuario)
        self.add_widget(self.mainchatscreen)
        self.add_widget(self.messagechat)
        self.add_widget(self.sendbutton)

    def sendMessage(self, nutton):
        mensagem =  self.messagechat.text
        self.messagechat.text = AliasProperty("")
        client_socket.send(bytes(mensagem,"utf8"))
        if mensagem =="{quit}":
            client_socket.close()
            app.stop()

    def receber(self):
        while True:
            try:
                msg = client_socket.recv(BUFSIZ).decode("utf8")
                self.mainchatscreen.readonly = BooleanProperty(False)
                self.mainchatscreen.insert_text(msg + "\n")
                self.mainchatscreen.readonly = BooleanProperty(True)
            except OSError:
                break




class ChatApp(App):
    def build(self):
        return ReceiveName()
if __name__ == '__main__':
    ChatApp().run()
