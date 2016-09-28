#! /usr/bin/env python
# -*- coding:utf-8 -*-

# Standard-Lib Imports
import socket
import threading
import logging
from timeit import default_timer as timer
import time
import sys, getopt
# Third-Party Imports

# CUSTOM Imports
from log import client_logger

SERVER_HOST = ('localhost', 5050)


class Client(threading.Thread):
    def __init__(self, ip='', port=0, server_host=SERVER_HOST):
        super(Client, self).__init__()
        self.ip = ip
        self.port = port
        self.server_host = server_host
        self.logger = logging.getLogger('ClientLog')

    def send_messages(self):
        while True:
            start = timer()
            msg = 'Hello World'.encode()
            self.logger.debug("[Enviando: %s]",
                              msg)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self.ip, self.port))
            sock.sendto(msg, self.server_host)
            self.logger.debug("[Enviado]")
            self.logger.debug("[Recibiendo respuesta...]")
            data = sock.recv(1024)
            end = timer()
            self.logger.info("[Recibido: %s] -> DIFF=%s",
                             data, end - start)
            time.sleep(1)

    def run(self):
        try:
            self.send_messages()
        except KeyboardInterrupt:
            self.logger.debug("You hit <Ctrl-C>, exiting...")
            self.logger.info("Client closed")


class MaxValueException(Exception):
    pass


def foo():
    pass

if __name__ == '__main__':
    quantity = 0
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hq:", ["quantity="])
    except getopt.GetoptError:
        valid_input = False
        while not valid_input:
            try:
                quantity = int(input('>> Ingrese cantidad de clientes a crear: '))
                if quantity > 256:
                    raise MaxValueException
                if quantity == 0:
                    client_logger.debug('Exiting client...')
                    exit(0)
            except MaxValueException:
                client_logger.debug('El valor máximo permitido es 256')
            except ValueError:
                client_logger.debug('Ingrese un valor numérico!')
            else:
                valid_input = True
    except MaxValueException:
        client_logger.debug('El valor máximo permitido es 256')
        sys.exit()
    except ValueError:
        client_logger.debug('Ingrese un valor numérico!')
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            print('client.py -q <quantity>')
            print('client.py --quantity <quantity>')
            sys.exit()
        elif opt in ("-q", "--quantity"):
            quantity = int(arg)

    for i in range(1, quantity + 1):
        client = Client(
            ip='127.0.0.{}'.format(i),
        )
        client.daemon = True
        client.start()

    while True:
        try:
            foo()
        except KeyboardInterrupt:
            print("Ctrl+C detected...")
            exit(0)
