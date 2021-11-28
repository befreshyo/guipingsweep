import socket

#create Socket
myServerSocket = socket.socket()

#get my local host address
localHost = socket.gethostname()

#specify a local Port to accept connections on
localPort = 5555

#bind mySocket to localHost and the specified localPort
myServerSocket.bind((localHost, localPort))

#begin Listening for connections
myServerSocket.listen(1)

#wait for a connection request
#synchronous call - program will halt until a connection is received
#once a connection is received, accept the connection and obtain the ipAddress of the connector
print ('Python-Forensics .... Waiting for Connection Request')
conn, clientInfo = myServerSocket.accept()

#print a message to indicate we have received a connection
print ('Connection Received From: '), clientInfo

#send a message to connector using the connection obj 'conn'
conn.send('Connection Confirmed: '+ 'IP: ' + clientInfo[0] + '  Port: ' + str(clientInfo[1]))

