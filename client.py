import os
import tkinter as tk
from tkinter import Tk, Text, Entry, Button, filedialog
import socket
from threading import Thread


host = '0.0.0.0'
port = 51301


ip = '10.100.5.142'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip,port))

pencere = Tk()
pencere.title("Bağlandı : "   +ip      +" "      + str(port))

message = Text(pencere, width=50)
message.grid(row=0,column=0, 
             padx=10, pady=10)

mesaj_giris= Entry(pencere, width=50)
mesaj_giris.insert(0, "Adınız")

mesaj_giris.grid(row=1, column=0, 
                 padx=10, pady=10)
mesaj_giris.focus()
mesaj_giris.selection_range(0, tk.END)

def mesaj_gonder():
    istemci_mesaji = mesaj_giris.get()
    message.insert(tk.END, '\n' + 'Sen :' + istemci_mesaji)
    client.send(istemci_mesaji.encode('utf8'))
    mesaj_giris.delete(0, tk.END)
    
btn_msg_gonder = Button(pencere, text='Gönder',
                        width=30, 
                        command=mesaj_gonder)
btn_msg_gonder.grid(row=2, column=0, 
                    padx=10, pady=10)
mesaj_giris.bind("<Return>", lambda event=None: btn_msg_gonder.invoke())
def dosya_gonder():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = os.path.basename(file_path)
        client.send(f"SEND_FILE:{file_name}".encode('utf8'))
        with open(file_path, 'rb') as file:
            file_data = file.read(1024)
            while file_data:
                client.send(file_data)
                file_data = file.read(1024)

        message.insert(tk.END, '\n' + f'Gönderilen Dosya: {file_name}')

btn_gozat = tk.Button(pencere, text='Gözat', width=30, command=dosya_gonder)
btn_gozat.grid(row=2, column=1, padx=10, pady=10)

def receive_file(server_socket, filename):
    with open(filename, 'wb') as file:
        while True:
            data = server_socket.recv(1024)
            if not data:
                break
            file.write(data)



def gelen_mesaj_kontrol():
    while True:
        server_msg = client.recv(1024).decode('utf8')
        if server_msg.startswith("SEND_FILE:"):
            # Dosyayı al ve kaydet
            file_name = server_msg.replace("SEND_FILE:", "")
            with open(file_name, 'wb') as file:
                file_data = client.recv(1024)
                while file_data:
                    file.write(file_data)
                    file_data = client.recv(1024)
            message.insert(tk.END, '\n' + f'Alınan Dosya: {file_name}')
        else:
            message.insert(tk.END, '\n' + server_msg)
            
            
            # Dosyayı almaya yönelik fonksiyon

        

recv_kontrol = Thread(target=gelen_mesaj_kontrol)
recv_kontrol.daemon = True
recv_kontrol.start()
pencere.mainloop()



