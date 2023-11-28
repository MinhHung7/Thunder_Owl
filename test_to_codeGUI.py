import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 2225
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def connect_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.settimeout(1000)
            client.connect(ADDR)
            print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

            # # Send the HELO or EHLO command
            # helo_command = "EHLO client\r\n"  # You can use HELO instead of EHLO if needed
            # client.send(helo_command.encode('utf-8'))

            # # Receive and print the server's response to the HELO or EHLO command
            # helo_response = client.recv(1024).decode('utf-8')
            # print(f"[SERVER] {helo_response}")

            # Receive and print the server's initial response
            initial_response = client.recv(1024).decode('utf-8')
            print(f"[SERVER] {initial_response}")

            # Send the MAIL FROM command
            mail_from_command = input("Enter your email address (MAIL FROM): ")
            mail_from_command = "MAIL FROM: " + mail_from_command + "\r\n"
            client.send(mail_from_command.encode('utf-8'))

            # Receive and print the server's response to the MAIL FROM command
            mail_from_response = client.recv(1024).decode('utf-8')
            print(f"[SERVER] {mail_from_response}")

            # Send the RCPT TO command
            recipient_email = input("Enter recipient's email address (RCPT TO): ")
            recipient_email = "RCPT TO: " + recipient_email + "\r\n"
            client.send(recipient_email.encode('utf-8'))

            # Receive and print the server's response to the RCPT TO command
            rcpt_to_response = client.recv(1024).decode('utf-8')
            print(f"[SERVER] {rcpt_to_response}")

            # Send DATA command
            data_command = "DATA\r\n"
            client.send(data_command.encode('utf-8'))

            # Receive and print the server's response to the DATA command
            data_response = client.recv(1024).decode('utf-8')
            print(f"[SERVER] {data_response}")

            # Send the message data
            subject = input("Enter email subject: ")
            message_content = input("Enter email content: ")

            message_data = (
                f"To: {recipient_email}\r\n"
                f"From: {mail_from_command}\r\n"
                f"Subject: {subject}\r\n"
                "\r\n"
                f"{message_content}\r\n"
                ".\r\n"  # This dot indicates the end of the message
            )
            client.send(message_data.encode('utf-8'))

            # Receive and print the server's response to the message data
            message_response = client.recv(1024).decode('utf-8')
            print(f"[SERVER] {message_response}")

            # Send the QUIT command
            quit_command = "QUIT\r\n"
            client.send(quit_command.encode('utf-8'))

            # Receive and print the server's response to the QUIT command
            quit_response = client.recv(1024).decode('utf-8')
            print(f"[SERVER] {quit_response}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    connect_server()
