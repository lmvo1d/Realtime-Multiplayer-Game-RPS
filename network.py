import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        with open("config.txt", "r") as f:
            self.server = f.readline().strip()
            self.port = int(f.readline().strip())
            
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        
        except socket.error as e:
            print("Error connecting to server: ", e)


    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(4096)
            try:
                return pickle.loads(reply)
            except pickle.UnpicklingError:
                return reply.decode()
        
        except socket.error as e:
            print("Error sending data: ", e)
            return None