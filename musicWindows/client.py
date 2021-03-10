#!/usr/bin/python3
import zmq,threading
from pygame import mixer, time
from os import path, listdir
from os.path import isfile, join


context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")
mixer.init()
songList = []


def main():
    userControler()


def printMenu():
    print('----- Welcome to our Music Service -----')
    print('Press l to list available songs')
    print('Press s to select a song')
    print('Press p to pause the song')
    print('Press r to resume')
    print('Press a to add a song to the playlist')
    print('Press e to exit')
    print('Press n to skip to next song')
    print('Press t to reproduce all the playlist')

def download(song):

    fileName = song.encode('utf-8')
    m = [b'download', fileName]
    socket.send_multipart(m)
    mR = socket.recv()
    returnMessage = ''
    if mR == b'00000':
        print('El archivo deseado no se encuentra disponible para descarga')
        returnMessage = 'error'
    else:
        # Evaluate if the file is already downloaded:
        mypath = r'C:\Users\athena\Documents\UTP\clientServer\music'
        downloadedSongs = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        returnMessage = 'ok'
        if song in downloadedSongs:
            pass
        else:
             # save it
             file = open(song, 'wb')
             file.write(mR)
             file.close()
             print('file {} has been received successfully'.format(m[1].decode('utf-8')))

    return returnMessage

def Play(song):
        # Play it
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
        message = download(song)
        if message == 'ok':
            songList.append(song)
            print(" " + song + " has been added to the playlist")
        else:
            print('Error adding song')
    except Exception as e:
        print(e)


def nextSong():
    global songList
    if len(songList):
        song = songList.pop(0)
        Play(song)
    else:
        print('No hay canciones en la lista de reproduccion por favor ingrese una')
        playList()


def allPlayList():
    global songList
    #If the list is not void
    if songList:
        print(songList)
        for song in songList:
            # songList.pop(0)
            print("Playing song:", song)
            Play(song)
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
            message = download(song)
            if message == 'ok':
                Play(song)
            else:
                print('Error playing the song')
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


if __name__ == "__main__":
    main()
