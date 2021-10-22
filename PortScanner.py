import inquirer
import re
import socket
import sys
import threading

from inquirer import errors
from queue import Queue

queue = Queue()
open_ports = []

def ip_alvo(nome):

    try:
        target = socket.gethostbyname(nome) #faz a resolução de nome
        print(f"\n[+] Escaneando IP de {nome}")

    except socket.gaierror:
        print("\n [+] Problema encontrado com o nome de Host")
        sys.exit()

    return target


def numberValidation(answers, current):
    if not re.match('^[0-9]+$', current):
        raise errors.ValidationError(
            '', reason='Número de thread inválido!')
    return True

def scan_port(port):

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((target, port))
        s.close
        return True

    except:
        return False


def scan_mode(mode):
    if(mode == "[1-1024]"):
        ports = range (1, 1024)

    elif(mode == "[1025-49152]"):
        ports = range (1025, 49152)

    elif(mode == "[49153-65535]"):
        ports = range (49153, 65535)

    elif(mode == "Todas as 65535 portas"):
        ports = range (1, 65535)

    list(map(queue.put, ports))


def scan_threads(threads):

    thread_list = []

    for _ in range(threads):
        thread = threading.Thread(target=threads_builder)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print("\n[+] Resumo das portas abertas:", open_ports)

def threads_builder():
    while not queue.empty():
        port = queue.get()
        if scan_port(port):
            print(f"\n [+] Porta {port} está aberta! Serviço: {socket.getservbyport(port) if socket.getservbyport(port) else 'Desconhecido'}")
            open_ports.append(port)


questions = [
    inquirer.Text('target', message="Forneça o alvo a ser escaneado"),
    inquirer.List('mode',
                  message="Quais portas você deseja escanear?",
                  choices=["[1-1024]", "[1025-49152]", "[49153-65535]", "Todas as 65535 portas"],
                  carousel=True
                  ),
    inquirer.Text('threads', message="Quantos threads devem ser utilizados?",
                  default=100, validate=numberValidation)
]

answers = inquirer.prompt(questions)

target = ip_alvo(answers["target"])
scan_mode(answers["mode"])
scan_threads(int(answers["threads"]))
