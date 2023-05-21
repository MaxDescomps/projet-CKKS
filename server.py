from keyboard_thread import *
from server_input import *
import socket
import threading
import hashlib
import json
import threading
import time
import datetime
import os

class Server():
    """Cloud server class"""

    def __init__(self):
        """Cloud server class constructor"""

        # Create Socket (TCP) Connection
        self.socket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM) 
        self.host = '127.0.0.1'
        self.port = 9999
        self.thread_count = 0
        self.hash_file = './HashTable.json' # Dictionnary holding login informations
        self.data_file = './DataTable.json' # Dictionnary holding server data
        self.kthread = KeyboardThread()

        # Load the HashTable
        try:
            with open(self.hash_file, 'r') as f:
                self.HashTable = json.load(f)
        except:
            self.HashTable = {} # Create the HashTable if needed

        # Load the DataTable
        try:
            with open(self.data_file, 'r') as f:
                self.DataTable = json.load(f)
        except:
            self.DataTable = {} # Create the HashTable if needed

        # Bind the socket
        try:
            self.socket.bind((self.host, self.port))
        except socket.error as e:
            print("Socket.bind: ", str(e))
        else:
            self.run()

    def run(self):
        """Handle the server once initialized"""

        self.socket.listen(2)
        print('Waiting for a Connection..')

        th_conn = threading.Thread(target=self.handle_conn_demand)
        th_conn.daemon = True
        th_conn.start()

        print("\nEnter \"exit\" to quit\n")

        # Server order main Loop
        while server_input[0] != "exit":
            time.sleep(1) # CPU break

        #todo: close every connections before closing socket
        self.close()

    def close(self):
        """Close the server properly"""

        # Save informations before turning off the server
        with open(self.hash_file, 'w') as f:
            json.dump(self.HashTable, f)
        
        with open(self.data_file, 'w') as f:
            json.dump(self.DataTable, f)

        self.socket.shutdown(socket.SHUT_RDWR) # Closes connections to the socket
        self.socket.close() # Closes the socket

    def threaded_client(self, connection: socket.socket):
        """
        Handle a client connecting to the server
        
        Args:
            connection(socket.socket): the client's socket
        """
        
        self.thread_count
        connection.send(str.encode('ENTER USERNAME : ')) # Request Username
        name = connection.recv(2048)
        connection.send(str.encode('ENTER PASSWORD : ')) # Request Password
        password = connection.recv(2048)
        password = password.decode()
        name = name.decode()
        password=hashlib.sha256(str.encode(password)).hexdigest() # Password hash using SHA256

        # REGISTERATION PHASE   
        # If new user,  regiter in Hashtable Dictionary  
        if name not in self.HashTable:
            self.HashTable[name]=password
            connection.send(str.encode('Registeration Successful')) 
            print('Registered : ',name)
            print("{:<8} {:<20}".format('USER','PASSWORD'))
            for k, v in self.HashTable.items():
                label, num = k,v
                print("{:<8} {:<20}".format(label, num))
            print("-------------------------------------------")
            
        # If already existing user, check if the entered password is correct
        else:
            if(self.HashTable[name] == password):
                connection.send(str.encode('Connection Successful')) # Response Code for Connected Client 
                print('Connected : ',name)
                
                # Main loop of communication with a client
                msg = True

                while msg:
                    msg = connection.recv(2048)
                    if msg:
                        msg = msg.decode()

                        if msg[0:6] == '/send ':
                            info = (msg[6:]).split("\n", 1)
                            file = open(os.path.join("database", info[0]),"w")
                            file.write(info[1])
                            file.close()

                            print(f"{name}: /send {info[0]}")

                            if name not in self.DataTable:
                                self.DataTable[name] = []

                            self.DataTable[name].append(f"/send {info[0]}")

                            file = open("logs.txt", "a")
                            file.write(f"({datetime.datetime.now()}) {name}: /send {info[0]}\n")
                            file.close()
                        else:
                            print(f"{name}: {msg}")

                            if name not in self.DataTable:
                                self.DataTable[name] = []

                            self.DataTable[name].append(msg)

                            file = open("logs.txt", "a")
                            file.write(f"({datetime.datetime.now()}) {name}: {msg}\n")
                            file.close()

                        #print(self.DataTable)

            else:
                connection.send(str.encode('Login Failed')) # Response code for login failed
                print('Connection denied : ',name)

        
        # End of communication with a client
        self.thread_count -= 1
        connection.close()

    def handle_conn_demand(self):
        """Handle connection demand"""
        
        while True:
            # Blocking function waiting for a client
            Client, address = self.socket.accept()

            client_handler = threading.Thread(target=self.threaded_client, args=(Client,))

            client_handler.start()
            self.thread_count += 1

            print('Connection Request: ' + str(self.thread_count))

Server()