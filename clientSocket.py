import socket
MAX_BUFFER = 1024

#create a socket
myClientSocket = socket.socket()

#get my local host address
localHost = socket.gethostname()

#specify a local Port to attempt a connection
localPort = 5555

#attempt a connection to my localHost and localPort
myClientSocket.connect((localHost, localPort))

#if connection is successful, wait for a reply
msg = myClientSocket.recv(MAX_BUFFER)
print(msg)

myClientSocket.close()
