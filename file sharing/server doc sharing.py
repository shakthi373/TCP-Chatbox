import socket
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.240.1', 59000))
server.listen()

print("Server is ready to receive files.")

def receive_file(client):
    try:
        message = client.recv(1024).decode('utf-8')
        file_name = message.split(' ')[1]
        with open(file_name, 'wb') as file:
            while True:
                file_data = client.recv(1024)
                if not file_data:
                    break
                file.write(file_data)
        print(f"Received file: {file_name}")
    except Exception as e:
        print(f"Error occurred while receiving the file: {e}")
    finally:
        client.close()

while True:
    client, address = server.accept()
    print(f"Connected with {address}")

    alias = client.recv(1024).decode('utf-8')

    while True:
        message = client.recv(1024).decode('utf-8')

        if message.startswith('/file'):
            receive_file(client)
        else:
            print(message)
