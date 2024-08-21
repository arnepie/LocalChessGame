import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ""  # Insert Wi-Fi ip address
        self.port = 5555  # Free port
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            # Add list or string to the data so the server can decode it
            if type(data) == list:
                serialized_data = b'LIST' + pickle.dumps(data)
                self.client.send(serialized_data)
            else:
                string_data = b'STRING' + str.encode(data)
                self.client.send(string_data)
            return pickle.loads(self.client.recv(2048*1028))
        except socket.error as e:
            print(e)
