import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
machine = socket.gethostbyname(socket.gethostname())
port = 9999

server.bind((machine, port))
server.listen()

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

sender()
