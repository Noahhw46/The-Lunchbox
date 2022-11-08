import socket

class Proxy:
    def __init__(self):
        self.host = 'host:port'
        self.port = 80
        self.buffer_size = 4096
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

    def run(self):
        while True:
            client, address = self.socket.accept()
            data = client.recv(self.buffer_size)
            if data:
                print(data)
                client.send(data)
            client.close()

if __name__ == '__main__':
    proxy = Proxy()
    proxy.run()