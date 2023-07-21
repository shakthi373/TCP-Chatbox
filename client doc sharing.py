import threading
import socket
import os

alias = input('Choose an alias >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('10.30.201.15', 59000))

def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except Exception as e:
            print(f'Error: {e}')
            client.close()
            break

def client_send():
    while True:
        user_input = input()
        if user_input.startswith('/sendfile'):
            file_path = user_input.split(' ')[1]
            if os.path.isfile(file_path):
                send_file(file_path)
            else:
                print("File not found.")
        else:
            message = f'{alias}: {user_input}'
            client.send(message.encode('utf-8'))

def send_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
        file_name = file_path.split('/')[-1]
        client.send(f'/file {file_name}'.encode('utf-8'))
        client.sendall(file_data)
        print(f"{file_name} sent successfully.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"Error occurred while sending the file: {e}")

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
