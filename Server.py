import socket
import threading

HOST = '192.168.247.169'  # Localhost
PORT = 12345

clients = [None, None]
ships_received = [False, False]
turn = 0  # Keeps track of whose turn it is

def handle_client(conn, player_id):
    conn.sendall(f"You are Player {player_id}".encode())
    opponent = 1 - player_id

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            if data.startswith("SHIPS"):
                ships = data.split(" ", 1)[1]
                print(f"[Player {player_id}] SHIPS {ships}")
                ships_received[player_id] = True
                if all(ships_received) and clients[opponent]:
                    clients[opponent].sendall("READY".encode())
                    conn.sendall("READY".encode())
                continue

            if data.startswith("FIRE") or data.startswith("RESULT"):
                if clients[opponent]:
                    clients[opponent].sendall(data.encode())

            if data.startswith("VICTORY"):
                if clients[opponent]:
                    clients[opponent].sendall("VICTORY".encode())

        except ConnectionResetError:
            print(f"Player {player_id} forcibly disconnected")
            break
        except Exception as e:
            print(f"Error handling player {player_id}: {e}")
            break

    conn.close()
    print(f"Player {player_id} disconnected")
    clients[player_id] = None
    ships_received[player_id] = False

def start_server():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(2)
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        for i in range(2):
            if clients[i] is None:
                clients[i] = conn
                print(f"[NEW CONNECTION] Player {i} connected from {addr}")
                threading.Thread(target=handle_client, args=(conn, i), daemon=True).start()
                break

        if all(clients):
            print("[READY] Both players connected. Waiting for ship placements...")

if __name__ == "__main__":
    start_server()
