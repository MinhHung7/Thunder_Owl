import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
machine = socket.gethostbyname(socket.gethostname())
port = 9999

client.connect((machine, port))

def receiver():
    while True:
        print("Receiving the file from the server")
        print("Creating the file to save the data")
        with open("Nguyễn Minh Hưng (Résume).png", "wb") as f:
            while True:
                data = client.recv(1024)
                if not data:
                    break
                f.write(data)
            print("Data has been received")
        break

receiver()
