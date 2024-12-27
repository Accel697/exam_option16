import socket


def client_program():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 666))

    while True:
        print("\nМеню:")
        print("1. Записать данные (введите 'write Фамилия Имя Отчество, Возраст')")
        print("2. Прочитать данные (введите 'read')")
        print("3. Выход (введите 'exit')")

        option = input("Выберите действие: ")

        if option.startswith('write'):
            client.send(option.encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            print(response)

        elif option == 'read':
            client.send(option.encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            print("Данные из файла:")
            print(response)

        elif option == 'exit':
            client.send(option.encode('utf-8'))
            break

        else:
            print("Неверный ввод.")

    client.close()


if __name__ == '__main__':
    client_program()
