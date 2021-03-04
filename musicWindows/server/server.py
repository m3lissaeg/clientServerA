#!/usr/bin/python3
import zmq, os 
from os import listdir
from os.path import isfile, join


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    
    m = socket.recv_multipart()
    res = ''
    if m[0] == b'download':
        # send filename m['fileName']
        print(isfile(m[1].decode('utf-8')))
        if isfile(m[1].decode('utf-8')):

            file = open(m[1].decode("utf-8"), 'rb')

            # Utilizamos os.stat para saber el estado de un path en particular
            file_stats = os.stat(m[1])

            print(f'File Size in Bytes is {file_stats.st_size}')

            fileSize = file_stats.st_size
            
            res = file.read(fileSize)
            
            socket.send(res)
            print('Succesful Download')
        else:
            socket.send_string('00000')
    
    elif m[0] == b'upload':

        if m[2] == b'error':
            res= 'Try again with a valid file'
        
        else:
            # recv stream and save it to the server: open it in write bytes mode
            file = open(m[1].decode("utf-8"), 'wb')
        
            file.write(m[2])
            file.close()
            print('file {} has been uploaded successfully'.format(m[1]))

            res = 'Successful Upload'
        socket.send_string(res)

    elif m[0] == b'list':
        #list all files:
        mypath = r'C:\Users\athena\Documents\UTP\clientServer\music\server'
        res = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        socket.send_string(str(res))
        print(res)
    else:
        res = 'Error. Try again with a valid request'
        socket.send_string(res)
