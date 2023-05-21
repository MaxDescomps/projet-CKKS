import socket
import pickle
import os

# System call
os.system("")

class style:
    END = '\33[0m'
    BOLD = '\33[1m'
    ITALIC = '\33[3m'
    URL = '\33[4m'
    BLINK = '\33[5m'
    BLINK2 = '\33[6m'
    SELECTED = '\33[7m'

    BLACK = '\33[30m'
    RED = '\33[31m'
    GREEN = '\33[32m'
    YELLOW = '\33[33m'
    BLUE = '\33[34m'
    VIOLET = '\33[35m'
    BEIGE = '\33[36m'
    WHITE = '\33[37m'

    BLACKBG = '\33[40m'
    REDBG = '\33[41m'
    GREENBG = '\33[42m'
    YELLOWBG = '\33[43m'
    BLUEBG = '\33[44m'
    VIOLETBG = '\33[45m'
    BEIGEBG = '\33[46m'
    WHITEBG = '\33[47m'

    GREY = '\33[90m'
    RED2 = '\33[91m'
    GREEN2 = '\33[92m'
    YELLOW2 = '\33[93m'
    BLUE2 = '\33[94m'
    VIOLET2 = '\33[95m'
    BEIGE2 = '\33[96m'
    WHITE2 = '\33[97m'

    GREYBG = '\33[100m'
    REDBG2 = '\33[101m'
    GREENBG2 = '\33[102m'
    YELLOWBG2 = '\33[103m'
    BLUEBG2 = '\33[104m'
    VIOLETBG2 = '\33[105m'
    BEIGEBG2 = '\33[106m'
    WHITEBG2 = '\33[107m'

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
            if msg:
                if msg[0] == '/':
                    if msg == '/ls':
                        ls = os.listdir()
                        for li in ls:
                            print(li)
                    elif msg[0:4] == '/ls ':
                        if os.path.exists(msg[4:]) and os.path.isdir(msg[4:]):
                            ls = os.listdir(msg[4:])
                            for li in ls:
                                print(li)
                        else:
                            print(f"{style.RED}Path not found{style.END}")
                    elif msg == '/cwd':
                        print(os.getcwd())
                    elif msg[0:4] == '/cd ':
                        if os.path.exists(msg[4:]) and os.path.isdir(msg[4:]):
                            os.chdir(msg[4:])
                        else:
                            print(f"{style.RED}Path not found{style.END}")
                    elif msg[0:6] == '/send ':
                        info = (msg[6:]).split(" ")
                        if len(info) == 2:
                            if os.path.exists(info[0]) and os.path.isfile(info[0]):
                                file = open(info[0], "r")
                                data = file.read()
                                file.close()
                                self.socket.send(str.encode(f"/send {info[1]}\n{data}"))
                            else:
                                print(f"{style.RED}File not found{style.END}")
                        else:
                            print(f"{style.RED}Number of parameters incorrect{style.END}")
                    elif msg[0:5] == '/srv ':
                        self.socket.send(str.encode(msg))
                        m = self.socket.recv(2048)
                        m = m.decode()
                        print(m)
                    else:
                        print(f"{style.RED}Command unknown or incomplete{style.END}")
                else:
                    self.socket.send(str.encode(msg))

Client()