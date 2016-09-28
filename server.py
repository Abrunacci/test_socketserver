#! /usr/bin/env python
# Standard-Lib Imports
import socketserver
import threading
import logging
from timeit import default_timer as timer
import time
# Third-Party Imports

# CUSTOM Imports
from log import server_logger


class UDPHandler(threading.Thread, socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server, action_time=1):
        self.logger = logging.getLogger('ServerLog')
        self.socket = request[1]
        self.data = request[0]
        self.turnstile = None
        self.card = None
        self.id_tag = ""
        self.action_time = action_time
        socketserver.BaseRequestHandler.__init__(self,
                                                 request,
                                                 client_address,
                                                 server)
        return

    def setup(self):
        return socketserver.BaseRequestHandler.setup(self)

    def send_reply(self):
        start = timer()
        self.logger.debug("[Respondiendo: %s to %s]",
                          self.data, self.client_address)
        time.sleep(self.action_time)
        self.socket.sendto(
            self.data, self.client_address)
        end = timer()
        self.logger.debug("[Respondido a %s] -> DIFF=%s",
                          self.client_address,
                          end - start)
        return

    def handle(self):
        self.send_reply()
        #t = threading.Thread(target=self.send_reply)
        #t.start()

    def finish(self):
        return socketserver.BaseRequestHandler.finish(self)


class Server(socketserver.ThreadingMixIn, socketserver.UDPServer):
    def __init__(self, ip='', port='', timeout=2, handler_class=UDPHandler):
        self.logger = logging.getLogger('ServerLog')
        self.ip = '0.0.0.0' if not ip else ip
        self.port = port
        self.timeout = timeout
        server_address = (ip, port)
        socketserver.UDPServer.__init__(self, server_address, handler_class)

    def server_activate(self):
        socketserver.UDPServer.server_activate(self)
        return

    def serve_forever(self):
        self.logger.debug("Starting server, hit <Ctrl-C> to quit")
        self.logger.debug("Logging is working")
        while True:
            self.handle_request()
        return

    def handle_request(self):
        return socketserver.UDPServer.handle_request(self)

    def verify_request(self, request, client_address):
        return socketserver.UDPServer.verify_request(self, request,
                                                     client_address)

    def process_request(self, request, client_address):
        return socketserver.UDPServer.process_request(self, request,
                                                      client_address)

    def server_close(self):
        return socketserver.UDPServer.server_close(self)

    def finish_request(self, request, client_address):
        return socketserver.UDPServer.finish_request(self, request,
                                                     client_address)

    def close_request(self, request_address):
        return socketserver.UDPServer.close_request(self, request_address)


class ServerMagic(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

if __name__ == '__main__':
    server = ServerMagic(('0.0.0.0', 5050), UDPHandler)
    #server = Server(ip='0.0.0.0', port=5050)
    try:

        th = threading.Thread(target=server.serve_forever())
        th.daemon = True
        th.start()
    except KeyboardInterrupt:
        server_logger.debug("You hit <Ctrl-C>, exiting...")
        server_logger.info("Closing server")
        server.server_close()
        server_logger.info("Server closed")
