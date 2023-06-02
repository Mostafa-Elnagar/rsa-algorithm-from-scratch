import socket 
import threading

import rsa

ADDR = "127.0.0.1"
PORT = 9999
BIND = (ADDR, PORT)

public_key, private_key = rsa.gen_keys(16)
public_partener = None 

choice = input("Do you want to host (1) or to connect (2):: ")

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(BIND)
    server.listen()

    client, _ = server.accept()
    client.send(rsa.pack(public_key).encode())
    public_partener = rsa.unpack(client.recv(1024).decode())

elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(BIND)
    public_partener = rsa.unpack(client.recv(1024).decode())
    client.send(rsa.pack(public_key).encode())

else:
    exit() 

def sending_messages(c):
    while True:
        message = input("")
        if "$hacker" not in message:
            encrypted = rsa.pack(rsa.encrypt(message, public_partener)).encode()
            c.send(encrypted)
        else:
            c.send(message.encode())
            
        print("You: " + message)

def recieving_messages(c):
    while True:
        recieved = c.recv(1024).decode()
        try:
            recieved = rsa.decrypt(rsa.unpack(recieved), private_key)
        except:
            pass
        print("partner: " + recieved)


threading.Thread(target=sending_messages, args=(client, )).start()
threading.Thread(target=recieving_messages, args=(client, )).start()