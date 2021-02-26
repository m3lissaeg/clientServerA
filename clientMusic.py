#!/usr/bin/python3
import zmq
import json
import os

def Main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5555")
    Request(socket)

def Request(socket):
    print('Enter the operation:')
    peticion = int(input('1.Upload   2.Download    3.List = '))

    if peticion == 1:
        # upload
        fileBytes = ''
        fileName = b'up.u'

        if os.path.isfile(fileName.decode('utf-8')):
            file_stats = os.stat(fileName.decode('utf-8'))
            print(f'File Size in Bytes is {file_stats.st_size}')

            fileSize = file_stats.st_size
            # Guardamos en una variable el archivo ubicado en la posicion 1 de m en modo read binary
            file = open(fileName.decode('utf-8'), 'rb')
            fileBytes = file.read(fileSize)
            # print(fileBytes)
        else:
            print('Error. The file requested to upload doesnt exist')
            fileBytes = b'error'

        m = [b'upload', fileName, fileBytes]

        socket.send_multipart(m)
        # mR = message received
        mR = socket.recv()
        print('{}'.format(mR.decode('utf-8'))) 

    elif peticion == 2:
        #download
        fileName = b'test.t'
        m = [b'download', fileName]
        socket.send_multipart(m)
        # mR = message received
        mR = socket.recv()
        if mR == b'Error el archivo deseado no se encuentra disponible para descarga':
            print(mR)
        else:
            # save the file: open it in write bytes mode
            file = open(fileName.decode('utf-8'), 'wb')
            file.write(mR)
            file.close()
            print('file {} has been received successfully'.format(m[1].decode('utf-8')))
    
    elif peticion == 3:
        # List elements in the server
        m = [b'list']
        socket.send_multipart(m)
        mR = socket.recv_multipart()
        print(mR)
    else:
        print('Wrong option. Try again with a valid option: 1 or 2')

if __name__ == "__main__":
   while True:
       Main() 