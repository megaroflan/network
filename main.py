import re
import sys
import subprocess
import json
from urllib.request import urlopen

regexIP = re.compile("\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}")


def get_ip_trace_rt(name: str) -> list:
    """
    Возвращает список IP во время трассировки маршрута
    """
    process = subprocess.Popen(["tracert", name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = process.communicate()[0].decode("cp866")
    return regexIP.findall(result)


def is_grey_ip(ip: str) -> bool:
    ip_octates = list(map(int, ip.split('.')))
    if ((ip_octates[0] == 10) or
            (ip_octates[0] == 172 and 16 <= ip_octates[1] <= 31) or
            (ip_octates[0] == 192 and ip_octates[1] == 168) or
            (ip_octates[0] == 100 and 64 <= ip_octates[1] <= 127)):
        return True
    else:
        return False


def get_info_by_ip(ip: str) -> tuple:
    """
    Функция для получения информации об IP-адресе посредством запроса к сервису ip-api.com.
    Возвращает tuple с IP, ASN, Country и Provider.
    """
    if not is_grey_ip(ip):
        try:
            with urlopen(f"http://ip-api.com/json/{ip}") as response:
                site_data = response.read().decode('utf-8')
                site_json = json.loads(site_data)

                ip = site_json["query"]
                as_name = site_json["as"][2:7]
                country = site_json["countryCode"]
                provider = site_json["org"]

                return ip, as_name, country, provider
        except Exception:
            return ip, '', '', ''


def print_route(ips: list) -> None:
    number = 1
    for i in ips:
        info = get_info_by_ip(i)
        if info is not None and info[1]:
            print(f'N={number}, IP={info[0]}, ASN={info[1]}, Country={info[2]}, Provider={info[3]}')
            number += 1


def main():
    """
    На вход подаётся доменное имя или IP-адрес из аргументов командной строки,
    выполняет трассировку маршрута до указанного адреса
    и выводит информацию об IP-адресах
    IP, ASN, Country, Provider
    """
    if len(sys.argv) < 2:
        print('Usage: python main.py <domain name or ip>')
        return
    ips = get_ip_trace_rt(sys.argv[1])
    print_route(ips)


if __name__ == '__main__':
    main()
