import socket
import re
import argparse
from multiprocessing import Process
import sys


class PortScanner:
    def __init__(self, ip, start, end):
        self.ip = ip
        self.start = start
        self.end = end
        self.pattern_ip = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

    def udp_scanner(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            try:
                sock.sendto(b"", (self.ip, port))
                sock.settimeout(1)
                sock.recvfrom(1024)
                print(f"UDP: порт {port} открыт")
            except socket.timeout:
                print(f"UDP: порт {port} открыт")
            except:
                pass

    def tcp_scanner(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.05)
            try:
                sock.connect((self.ip, port))
            except:
                pass
            else:
                print(f"TCP: порт {port} открыт")

    def check_ip(self):
        if not re.search(self.pattern_ip, self.ip):
            print("Некорректный ip адрес")
            sys.exit()

    def scan_ports(self):
        self.check_ip()
        for i in range(self.start, self.end):
            proc_tcp = Process(target=self.tcp_scanner, args=(i,))
            proc_udp = Process(target=self.udp_scanner, args=(i,))
            proc_tcp.start()
            proc_udp.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP and UDP scanner")
    parser.add_argument('-i', "--ip", help="ip", required=True)
    parser.add_argument("-s", "--start", help="Beginning of the range", required=True, type=int)
    parser.add_argument("-e", "--end", help="Ending of the range", required=True, type=int)
    args = parser.parse_args()

    scanner = PortScanner(args.ip, args.start, args.end)
    scanner.scan_ports()