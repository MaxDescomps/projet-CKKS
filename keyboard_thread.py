import threading
from server_input import *

class KeyboardThread(threading.Thread):
    """Keyboard input thread class"""

    def __init__(self):
        """KeyboardThread class constructor"""

        super().__init__()

        self.daemon = True # Closes the thread if the parent thread ends
        self.start()

    def run(self):
        """Waits for an input"""

        global server_input # Refers to the global list server_input

        while True:
            server_input[0] = input()
            print('You Entered:', server_input[0])