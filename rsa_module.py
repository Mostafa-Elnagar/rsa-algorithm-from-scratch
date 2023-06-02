
import socket 
import threading
import rsa

ADDR = "127.0.0.1"
PORT = 9999
BIND = (ADDR, PORT)

class Client:
    def __init__(self, address, port,encryption_key_length: int=512) -> None:
        self.pub_key, self.priv_key = rsa.gen_keys(encryption_key_length) 
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._id = 
        self.address_bind = address, port 


    def encrypt(self) -> None:
        pass 

    def decrypt(self) -> None:
        pass

    def get_pub_key(self) -> tuple[int, int]:
        return self.pub_key
    
    def get_priv_key(self) -> tuple[int, int]:
        return self.priv_key
    
    def reset_keys(self, key_length: int=512) -> tuple[tuple[int, int], tuple[int, int]]:
        self.pub_key, self.priv_key = rsa.gen_keys(key_length)
        return self.pub_key, self.priv_key
    
    def connect(self):
        pass

    def disconnect(self):
        pass

    def sending_messages(c):
        try:
            while True:
                message = input("")
                if "kosomk" not in message:
                    encrypted = rsa.encrypt(message.encode(), public_partener)
                    c.send(encrypted)
                else:
                    c.send(message.encode())

                print("You: " + message)
        except KeyboardInterrupt:
            print(f"left")

    

public_key, private_key = rsa.newkeys(1024)
public_partener = None 

choice = input("Do you want to host (1) or to connect (2):: ")

if choice == "1": 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(BIND)
    server.listen()

    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partener = rsa.PublicKey.load_pkcs1(client.recv(1024))


elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(BIND)
    public_partener = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))

else:
    exit() 

def sending_messages(c):
    while True:
        message = input("")
        if "kosomk" not in message:
            encrypted = rsa.encrypt(message.encode(), public_partener)
            c.send(encrypted)
        else:
            c.send(message.encode())

        print("You: " + message)

def recieving_messages(c):
    while True:
        recieved = c.recv(1024).decode
        try:
            recieved = rsa.decrypt(recieved, private_key)
        except:
            pass
        print("partner: " + recieved.decode())


threading.Thread(target=sending_messages, args=(client, )).start()
threading.Thread(target=recieving_messages, args=(client, )).start()