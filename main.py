from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
from tkinter.colorchooser import *

###  O método receber() é um loop contínuo onde o cliente fica esperando um
###  receive(recv() no cleinte, send() no servidor) pra atualizar a tela
###  de chat principal, inserindo o que receber no fim do texto e quebrando a
###  linha logo em seguida.
def receber():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            mainchatscreen.insert(END, msg + "\n")
        except OSError:
            break
###  O método callback() é chamado DEPOIS de receber o nome do cliente no começo
###  do programa, no exato momento que o botão 'eh isto' é apertado; o que tiver
###  na lacuna do começo é enviado pro servidor como o nome do cliente conectado.
###  Tem várias gambiarras, mas vamos lá:
def callback():
    client_socket.send(bytes(nome.get(),"utf8"))    #essa linha envia nome do user pro server;
    name.set(nome.get())                            #essa linha atualiza a interface grafica com o seu nome
    frame1.pack_forget()                            #
    frame2.pack_forget()                            # essa série de pack_forgets
    frame3.pack_forget()                            # deleta todas as paradas da tela
    labelnome.pack_forget()                         # depois que é enviado o nome.
    nome.pack_forget()                              # e também porque no tkinter,
    botaodonome.pack_forget()                       # usar metodos de geometria diferentes
    app.pack_forget()                               # bugam A PORRA INTEIRA
    app.grid()                                      # (no caso, apago todos os pack() que fiz
    nomedeusuario.config(text = name.get())         # pra usar grid() com intenção de estilizar bonitinho
    createChatBox()                                 # nessa ultima linha, mando o programa criar o chat em si

def createChatBox():                                                      #essa função põe todos os elementos do chat no lugar que eu quero
    mainchatscreen.grid(row = 0, column = 0, sticky = E, columnspan = 5)
    messagechat.grid(row = 1, column = 3,)
    sendbutton.grid(row = 1, column = 4)


    labelmensagem.grid(row = 1, column = 2)
    nomedeusuario.grid(row = 1, column = 0)

def sendMessage(event=None):                    #essa função recebe event = none como argumento porque o tkinter acaba passando sem querer coisa errada
    mensagem =  messagechat.get()               #messagechat é a mensagem que está escrita na lacuna, que voce quer enviar
    messagechat.delete(0,END)                   #depis que é enviada a mensagem, essa linha limpa a lacuna(do index 0 até o fim do que tiver)
    client_socket.send(bytes(mensagem,"utf8"))  #envia a mensagem pro servidor
    if mensagem =="{quit}":                     #mas se a mensagem for {quit}(com as chaves), fecha  aconexão e fecha o programa
        client_socket.close()
        root.quit()

def on_closing(event=None):             #essa ultima função GARANTE que ao tentar fechar apertando o x da janela,
    messagechat.delete(0,END)           # é enviado antes pro servidor uma mensagem de {quit}, pra fechar a conexão também
    messagechat.insert(END,"{quit}")    # se não o programa fecha mas a conexão fica aberta
    sendMessage()

    #agora os comentários serão linha por linha, importantissimo


root = Tk()                                                                                                     #inicializa a tela principal do programa com o nome de root.
root.title("Teste")                                                                                             #título testo da janela
root.geometry("537x350")                                                                                        #tamanho da janela largura x altura
root.configure(background = "black")                                                                            #estilizando a janela pra deixar tudo preto
root.resizable(False, False)                                                                                    #não permitir que o usuario possa redimensionar a janela
app = Frame(root, bg = "black")                                                                                 #cria um widget em cima da tela root, com fundo preto(pra garantir)
name = StringVar()                                                                                              #se eu tivesse inicializado o name sem ser uma variavel do tkinter, a interface não ia atualizar pro nome que seria dado no começo do programa
app.pack()                                                                                                      #CONCEITO IMPORTANTE: a função .pack() é um dos jeitos de imprimir coisas na tela; pack em si é algo simples no sentido de ele não analisar muito onde, só a ordem.
frame1 = Frame(root, bg = "black")                                                                              #eu não sabia como centralizar o prompt de nome do usuario no começo do programa, então criei 3 frames(1 2 e 3) a fim de dividir a tela igualmente
frame1.pack(expand=True, fill=NONE)                                                                             #imprimo frame 1 na tela principal root
frame2 = Frame(root, bg = "black")                                                                              #frame2 como vai ficar exatamente no meio entre os dois outros frames, uso ele como referencia pra plantar a próxima linha
labelnome = Label(frame2, text = "...seu nome, por favor.", bg = "black", fg = "white")                         #crio o texto que pede nome no começo, boto pra ficar em cima do frame 2
labelnome.pack(padx = 0, pady = 0)                                                                              #imprimo o texto da linha de cima pra ficar centralizado no frame 2
nome = Entry(frame2, bg = "black", fg = "white")                                                                #crio a lacuna que vai receber o nome
nome.pack()                                                                                                     #imprimo a lacuna; como o metodo pack() é o mais simples, ele coloca onde couber e centralizado com base no pack anterior
nome.focus_set()                                                                                                #garanto que a lacuna ja pode ser digitada em cima sem precisar clicar de cara
botaodonome = Button(frame2, bg = "black", fg = "white",text = "eh isto", command = callback)                   #botão que executa o método callback(), que armazena e envia o nome pro servidor
botaodonome.pack()                                                                                              #imprimo o botao, centralizado e embaixo do ultimo pack(a lacuna, nesse caso)
frame2.pack(anchor=CENTER)                                                                                      #imprimo o frame 2 que vai imprimir os tres negocios ao mesmo tempo( o texto, a lacuna e o botão)
frame3 = Frame(root, bg = "black")                                                                              #crio o terceiro frame que vai garantir que o frame 2 fique no meio e não na segunda metade da tela
frame3.pack(expand=True, fill=NONE)                                                                             #imprimo, expando para que o tamanho efetivo do frame 2 seja 0, mas ainda entre frame 1 e 3
nomedeusuario = Label(root, text = name, bg = "black", fg = "white")                                            #estipulo o nome de cada elemento da tela de chat principal; essa linha é o nome que voce digitou
mainchatscreen = Text(root, width=60, height=20, background = 'black', fg='white')                              #estipulo o tamanho da tela de chat principal, onde o cliente recebe o chat
messagechat = Entry(root, width = 40, bg = "black", fg = "white")                                               #lacuna de envio de mensagens
sendbutton = Button(root, text = "enviar", command = sendMessage, bg = "black", fg = "white")                   #botão de enviar a mensagem
refreshbutton = Button(root, text = "colorizar", bg = "black", fg = "white")                                    #botão não usado ainda mas que já criei pois pretendo botar cor no texto do chat
labelmensagem = Label(root, text = "msg ->",bg = "black", fg = "white")                                         #textinho apontando a lacuna de mensagens
messagechat.bind("<Return>", sendMessage)                                                                       #essa linha é legal: ligo a tecla enter com o método de enviar mensagem em referencia a lacuna de enviar mensagens
root.protocol("WM_DELETE_WINDOW", on_closing)                                                                   #aqui eu chamo o método on_closing() se o usuario tentar fechar a janela pelo x ou por alt f4, garantindo que feche a conexão antes






HOST = '179.100.92.218' #IP A SER CONECTADO
PORT = 33000            #PORTA A SE CONECTAR NO HOST

BUFSIZ = 1024           #pra referencia qual o tamanho MÁXIMO de dados que vai ser enviado e recebido
ADDR = (HOST, PORT)     #a ser usado com o método connect da biblioteca socket do python

client_socket = socket(AF_INET, SOCK_STREAM)  #ainda preciso entender HUE
client_socket.connect(ADDR)                   #é isso

receive_thread = Thread(target=receber)        #cria uma thread de loop infinito do método receber(), pra ficar esperando e recebendo coisa nova do chat
receive_thread.start()                         #começa a thread





root.mainloop()        #linha final necessária pra interface grafica ficar constantemente aberta na tela
