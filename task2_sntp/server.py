import socket
import struct
import configparser


class TimeServer:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')  # читаем конфигурационный файл
        self.offset = int(self.config.get('time', 'offset'))  # считываем значение смещения времени из конфига
        self.server_address = ('localhost', 123)  # адрес сервера и порт, на котором он будет прослушивать запросы

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # создаем UDP-сокет
        server_socket.bind(self.server_address)  # связываем сокет с адресом сервера

        print("Начало работы")  # выводим сообщение о запуске сервера

        try:
            while True:
                data, address = server_socket.recvfrom(1024)  # принимаем данные от клиента
                print(f"Получил запрос: {address[0]}:{address[1]}")

                # Получаем текущее время от надежного сервера точного времени
                try:
                    time_data = self.get_time()
                except Exception as e:
                    print(f"ошибка: {e}")
                    continue

                # Добавляем смещение к текущему времени
                modified_time = time_data + self.offset

                # Упаковываем измененное время в формат NTP
                ntp_epoch = 2208988800
                seconds, fraction = str(modified_time - ntp_epoch).split('.')
                ntp_data = struct.pack('!I', int(seconds)) + struct.pack('!I', round(float(fraction) * 2 ** 32))

                # Отправляем измененное время клиенту
                server_socket.sendto(ntp_data, address)

        except KeyboardInterrupt:
            print('Прервано')
            server_socket.close()

    def get_time(self):
        time_server = self.config.get('time', 'server', fallback='time.windows.com')
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.sendto(b'\x1b' + 47 * b'\0', (time_server, 123))  # отправляем запрос на сервер времени
        data, address = client.recvfrom(1024)  # принимаем ответ от сервера времени
        if data:
            data = data[40:]
            # Конвертируем время из формата NTP в обычный формат
            ntp_epoch = 2208988800
            seconds, fraction = struct.unpack('!I', data[:4])[0], struct.unpack('!I', data[4:])[0]
            timestamp = seconds + fraction / 2 ** 32
            return timestamp + ntp_epoch


time_server = TimeServer()
time_server.run()