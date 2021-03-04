#!/usr/bin/python3
from pygame import mixer
import os, zmq
from os import path, listdir
# os.environ['SDL_AUDIODRIVER'] = 'dsp'

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")

mixer.init()

def printMenu():
    print('----- Welcome to our Music Service -----')
    print('Press l to list available songs')
    print('Press s to select a song')
    print('Press p to pause the song')
    print('Press r to resume')
    print('Press a to add a song to the playlist')

    print('Press e to exit')

def downloadAndPlay(song):
    fileName = song.encode('utf-8')
    m = [b'download', fileName]
    socket.send_multipart(m)
    mR = socket.recv()
    if mR == b'00000':
        print('El archivo deseado no se encuentra disponible para descarga')
    else:
        # save it
        file = open(fileName.decode('utf-8'), 'wb')
        file.write(mR)
        file.close()
        print('file {} has been received successfully'.format(m[1].decode('utf-8')))
        # And play it
        mixer.music.load(song)
        mixer.music.set_volume(0.5)
        mixer.music.play()

def listSongs():
    # List elements in the server
    m = [b'list']
    socket.send_multipart(m)
    mR = socket.recv_multipart()

    return mR


while True:
    printMenu()
    opt = input('>>>')

    if opt=='p':
        mixer.music.pause()
    elif opt == 'r':
        mixer.music.unpause()
    elif opt == 's':
        # mixer.music.stop()
        song = str(input('Enter the name of the song: '))
        downloadAndPlay(song)
    elif opt == 'l':        
        print(listSongs())
    elif opt == 'r':
        mixer.music.stop()
        break

