from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
from tkinter.colorchooser import *



def receber():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            mainchatscreen.insert(END, msg + "\n")
        except OSError:
            break



def callback():
    client_socket.send(bytes(nome.get(),"utf8"))
    name.set(nome.get())
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()
    labelnome.pack_forget()
    nome.pack_forget()
    botaodonome.pack_forget()
    app.pack_forget()
    app.grid()
    nomedeusuario.config(text = name.get())
    createChatBox()

def createChatBox():
    mainchatscreen.grid(row = 0, column = 0, sticky = E, columnspan = 5)
    messagechat.grid(row = 1, column = 3,)
    sendbutton.grid(row = 1, column = 4)


    labelmensagem.grid(row = 1, column = 2)
    nomedeusuario.grid(row = 1, column = 0)

def sendMessage(event=None):
    mensagem =  messagechat.get()
    messagechat.delete(0,END)
    client_socket.send(bytes(mensagem,"utf8"))
    if mensagem =="{quit}":
        client_socket.close()
        root.quit()

def on_closing(event=None):
    messagechat.delete(0,END)
    messagechat.insert(END,"{quit}")
    sendMessage()




root = Tk()
root.title("Teste")
root.geometry("537x350")
root.configure(background = "black")
root.resizable(False, False)
app = Frame(root, bg = "black")
name = StringVar()
app.pack()
frame1 = Frame(root, bg = "black")
frame1.pack(expand=True, fill=NONE)
frame2 = Frame(root, bg = "black")
labelnome = Label(frame2, text = "...seu nome, por favor.", bg = "black", fg = "white")
labelnome.pack(padx = 0, pady = 0)
nome = Entry(frame2, bg = "black", fg = "white")
nome.pack()
nome.focus_set()
botaodonome = Button(frame2, bg = "black", fg = "white",text = "eh isto", command = callback)
botaodonome.pack()
frame2.pack(anchor=CENTER)
frame3 = Frame(root, bg = "black")
frame3.pack(expand=True, fill=NONE)
nomedeusuario = Label(root, text = name, bg = "black", fg = "white")
mainchatscreen = Text(root, width=60, height=20, background = 'black', fg='white')
messagechat = Entry(root, width = 40, bg = "black", fg = "white")
sendbutton = Button(root, text = "enviar", command = sendMessage, bg = "black", fg = "white")
refreshbutton = Button(root, text = "colorizar", bg = "black", fg = "white")
labelmensagem = Label(root, text = "msg ->",bg = "black", fg = "white")
messagechat.bind("<Return>", sendMessage)
root.protocol("WM_DELETE_WINDOW", on_closing)






HOST = '179.100.92.218'
PORT = 33000
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receber)
receive_thread.start()





root.mainloop()
