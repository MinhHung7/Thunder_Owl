import socket
import threading
import wikipedia

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

fileprocess = 0
def handle_client(conn, addr, ):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False

        elif(msg == "send file"):
            
            echoMsg = ""

        print(f"[{addr}] {msg}")
        # msg = f"Msg received: {msg}"
        msg = wikipedia.summary(msg, sentences=1)
        conn.send(msg.encode(FORMAT))

    conn.close()

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()



def sender():
    print(f"[{machine}] Waiting for the connection from the client")
    while True:
        client, address = server.accept()
        print("Client connected, sending the file now")

        with open("Nguyễn Minh Hưng (Résume).png", "rb") as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                client.send(data)
            print("Data sent successfully")

        client.close()

