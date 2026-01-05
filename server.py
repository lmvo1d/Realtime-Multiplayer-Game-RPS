import socket
from _thread import *
import sys
import pickle

from game import Game

with open("config.txt", "r") as f:
    server = f.readline().strip()
    port = int(f.readline().strip())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))
    sys.exit()

s.listen()
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0

def threaded_client(conn, p, gameId):
    global idCount

    conn.send(str.encode(str(p)))

    reply = ""

    while True:
        data = conn.recv(4096).decode()

        try:
            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset_went()
                    elif data != "get":
                        game.play(p, data)

                    reply = game

                    conn.sendall(pickle.dumps(reply))

            else:
                break

        except Exception as e:
            print(e)
            break
    
    print("Lost connection")

    try:
        del games[gameId]
        print("Closing Game", gameId)
        print("Removed game", gameId)
    except:
        pass

    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2

    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))