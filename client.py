import socket
import sys

print("~~~~~~~~~~~~~~Client~~~~~~~~~~~~~~")

try:
    SOCK = socket.socket()
    HOST = '127.0.0.1'
    PORT = 8000

    SOCK.connect((HOST, PORT))
except:
    print("Error connecting to server")
    sys.exit()

print("Enter commands for help.\n")
while True:
    INP = input("client => ")
    if INP == "":
        print("Invalid command")
        continue
    SOCK.send(str.encode(INP))
    print("server => " + str(SOCK.recv(4096), "utf-8"))
    if INP.lower() == "quit":
        sys.exit()
