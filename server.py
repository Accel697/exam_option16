import socket
import threading
import random
import os


def handle_client(client_socket, client_address):
    ip_filename = f"{client_address[0]}_client.txt"

    while True:
        request = client_socket.recv(1024).decode('utf-8')
        if request == 'exit':
            print(f"Клиент {client_address} отключен.")
            break

        if request.startswith('write'):
            client_data = request[6:]

            if len(client_data.split(', ')) != 4:
                client_socket.send(
                    "Ошибка: необходимо ввести все данные в формате 'Фамилия, Имя, Отчество, Возраст'.".encode('utf-8'))
                continue

            id = random.randint(1, 1000)
            lastname, firstname, middlename, age = client_data.split(', ')
            data_to_write = f"{id}\n{lastname}\n{firstname}\n{middlename}\n{age}\n"

            with open(ip_filename, 'w') as f:
                f.write(data_to_write)
            client_socket.send("Данные записаны.".encode('utf-8'))

        elif request == 'read':
            if os.path.exists(ip_filename):
                with open(ip_filename, 'r') as f:
                    data = f.readlines()
                    formatted_data = f"{data[0].strip()} {data[1].strip()} {data[2].strip()} {data[3].strip()}, {data[4].strip()}"
                client_socket.send(formatted_data.encode('utf-8'))
            else:
                client_socket.send("Файл не найден.".encode('utf-8'))

    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 666))
    server.listen(4)
    print("Сервер запущен и ожидает подключения...")

    while True:
        client_sock, addr = server.accept()
        print(f"Подключен клиент {addr}")
        thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        thread.start()


start_server()