import socket
import threading

HOST = '192.168.38.207'
PORT = 12345

def receive(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print("\n" + msg)
        except:
            break

def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    threading.Thread(target=receive, args=(sock,), daemon=True).start()

    while True:
        try:
            msg = input()
            if msg.lower() == 'exit':
                sock.close()
                break
            sock.sendall(msg.encode())
        except:
            break

if __name__ == "__main__":  # ✅ Fixed this line
    start_client()
