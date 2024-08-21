import socket
from _thread import *
import pickle
from game import GameState

server = ""  # Insert Wi-Fi ip address
port = 5555  # Free port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)


s.listen()
print("Waiting for a connection, Server Started")

connected = set()
games = {}  # Dictionary to keep track of the games
idCount = 0  # Starting idCount


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096)  # Receive data

            if gameId in games:  # Check if the game still exists
                game = games[gameId]

                if not data:
                    break
                else:
                    if data[:4] == b'LIST':
                        # Deserialize the list
                        received_data = pickle.loads(data[4:])
                        game.play(received_data)
                        print("playing")
                    elif data[:6] == b'STRING':
                        # Decode the string
                        received_data = data[6:].decode()
                        if received_data == "reset":
                            game.reset()
                    else:
                        print("Unknown data format received")
                        return None

                    # Send back the game class
                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    # If something went wrong, close and delete the game
    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game: ", gameId)
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
        games[gameId] = GameState(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        print(games[gameId].ready)
        print(gameId)
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))

