#!/usr/bin/python3
from pygame import mixer, time
import os, zmq, threading
from os import path, listdir

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")
mixer.init()
songList = []


def printMenu():
    print('----- Welcome to our Music Service -----')
    print('Press l to list available songs')
    print('Press s to select a song')
    print('Press p to pause the song')
    print('Press r to resume')
    print('Press a to add a song to the playlist')
    print('Press n to skip to next song')
    print('Press t to reproduce all the playlist')
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


def playList():
    global songList
    try:
        song = str(input("Please enter the name of the song>>> "))
        songList.append(song)
        print(" " + song + " ha sido agregada correctamente a la lista de reproduccion!")
    except Exception as e:
        print(e)


def nextSong():
    global songList
    if len(songList):
        song = songList.pop(0)
        downloadAndPlay(song)
    else:
        print('No hay canciones en la lista de reproduccion por favor ingrese una')
        playList()


def allPlayList():
    global songList
    #If the list is not void
    if songList:
        for song in songList:
            songList.pop(0)
            # print(songAux)
            print("Playing song:", song)
            downloadAndPlay(song)
            # Wait for the music to play before exiting 
            while mixer.music.get_busy():   
                time.Clock().tick(5)


def userControler():
    while True:
        printMenu()
        opt = input('>>>')

        if opt == 'p':
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
        elif opt == 'a':
            playList()
        elif opt == 'n':
            nextSong()
        elif opt == 't':
            t = threading.Thread(target=allPlayList)
            t.start()
            # t.join()

def main():
    userControler()

if __name__ == "__main__":
    main()
