import socket

SERVER = '127.0.0.1'
SERVER_POP3_PORT = '2000'
SERVER_SMTP_PORT = '1000'
FORMAT = "utf-8"
RECV_LENGTH = 1024

# Lệnh POP3
def send_the_content(server_socket):
    email_content = 'Subject: Test Email\r\n\r\nHello, this is a test email.\r\n'
    server_socket.sendall(email_content.encode(FORMAT))
def end(server_socket):
    server_socket.sendall(b'\r\n.\r\n')
def test_send_email():
    with socket.create_connection((SERVER, SERVER_SMTP_PORT)) as server_socket:
        # Receive the server's welcome message
        welcome_msg = server_socket.recv(RECV_LENGTH)
        print(welcome_msg.decode())

        command = input('Enter your command: ')
        while command != 'OUT':
            if command == 'CONTENT':
                send_the_content(server_socket)
                command = input('Enter your command: ')
                continue
            elif command == 'END':
                end(server_socket)
                command = input('Enter your command: ')
                continue
            server_socket.sendall(f'{command}\r\n'.encode(FORMAT))
            response = server_socket.recv(RECV_LENGTH)
            print(response.decode(FORMAT))
            command = input('Enter your command: ')

def test_receive_email():
    with socket.create_connection((SERVER, SERVER_POP3_PORT)) as server_socket:
        # Receive the server's welcome message
        welcome_msg = server_socket.recv(RECV_LENGTH)
        print(welcome_msg.decode())

        command = input('Enter your command: ')
        while command != 'OUT':
            server_socket.sendall(f'{command}\r\n'.encode(FORMAT))
            response = server_socket.recv(RECV_LENGTH)
            print(response.decode(FORMAT))
            command = input('Enter your command: ')


if __name__ == "__main__":
    test_receive_email()