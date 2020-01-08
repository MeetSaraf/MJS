import socket
import threading
import pandas as pd
from clientResponse import ClientResponse
from logger import log

class Server():
    """
        Class Server.
        Accept the client connections and respond.
    """
    def __init__(self):
        self.socket = socket.socket()
        self.clientConnections = []
        self.clientip = []
        self.clientthreads = {}
        self.clienthandler = {}
        reset_login = pd.DataFrame(columns=['username'])
        reset_login.to_csv("serverSession/loginUsers.csv", index=False)

        # accept connections
        log.info("Opening server at port 8000")
        try:
            self.socket.bind(("", 8000))
            self.socket.listen(6)
        except socket.error as msg:
            log.info("error: %s", msg)
        threading.Thread(target=self.acceptConnections, args=(), daemon=True).start()

        # run threads for client to communicate with multiple clients
        while True:
            for conn, address in zip(self.clientConnections, self.clientip):
                try:
                    if self.clientthreads[address] == 0:
                        threading.Thread(target = self.client, args=(conn, address), daemon=True).start()
                except Exception as exception:
                    log.info("Error : %s", exception)
                    pass

    def acceptConnections(self):
        """
            Accept the client connections.
        """
        while True:
            try:
                conn, address = self.socket.accept()
                self.socket.setblocking(1)
                self.clientConnections.append(conn)
                self.clientip.append(address)
                self.clientthreads[address] = 0
                self.clienthandler[address] = ClientResponse()
                log.info("Client connected from ip :" + address[0])
            except Exception as e:
                log.info("Error : %s", e)

    def client(self, conn, addr):
        """
            Response from client-response class.
        """
        try:
            self.clientthreads[addr] = 1
            client_res = str(conn.recv(4096), "utf-8")
            response = self.clienthandler[addr].get_response(client_res)
            conn.send(str.encode(response))
            self.clientthreads[addr] = 0
        except Exception as exception:
            self.clienthandler[addr].get_response("quit")
            log.info(exception)


if __name__ == '__main__':
    Server()
