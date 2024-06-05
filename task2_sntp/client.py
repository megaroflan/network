import socket
import struct
import datetime

server_address = ('localhost', 123)  # адрес сервера и порт, на котором он прослушивает запросы

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # создаем UDP-сокет

try:
    while True:
        message = input("Введите что-нибудь: ")  # ждем ввода сообщения от пользователя
        client_socket.sendto(message.encode(), server_address)  # отправляем сообщение на сервер

        data, address = client_socket.recvfrom(1024)  # принимаем измененное время от сервера
        seconds, fraction = struct.unpack('!I', data[:4])[0], struct.unpack('!I', data[4:])[0]
        timestamp = seconds + fraction / 2 ** 32

        # Преобразуем полученную временную метку в объект datetime
        dt = datetime.datetime.fromtimestamp(timestamp)

        print(f"Измененное время: {dt.strftime('%d %B %Y %H:%M:%S')}")  # выводим измененное время в человекочитаемом формате

except KeyboardInterrupt:
    print('Прервано')
    client_socket.close()