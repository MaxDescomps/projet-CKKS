import socket

class Client():
    """Client class"""

    def __init__(self):
        """Client class constructor"""

        # Uses IPV4 (AF_INET) and TCP (Sock_STREAM)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        """Connect the client to the server"""

        # Connection to the server
        self.socket.connect(('127.0.0.1', 9999))
        response = self.socket.recv(2048)

        # LOGIN
        # Input UserName
        name = input(response.decode())
        self.socket.send(str.encode(name))
        
        response = self.socket.recv(2048)

        # Input Password
        password = input(response.decode())	
        self.socket.send(str.encode(password))

        # Receive response 
        response = self.socket.recv(2048)
        response = response.decode()

        print(response)

        if response[0] != 'R': # If client did not Register for the first time it can use the server
            self.use_server()

        self.socket.close()

    def use_server(self):
        """Handle client once connected to the server"""
        msg = True

        while msg:
            msg = input()
            self.socket.send(str.encode(msg))

Client()