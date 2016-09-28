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


class UDPHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('ServerLog')
        self.socket = request[1]
        self.data = request[0]
        self.turnstile = None
        self.card = None
        self.id_tag = ""
        socketserver.BaseRequestHandler.__init__(self,
                                                 request,
                                                 client_address,
                                                 server)
        return

    def setup(self):
        return socketserver.BaseRequestHandler.setup(self)

    def handle(self):
        start = timer()
        self.socket.sendto(
            self.data, self.client_address)
        time.sleep(1)
        end = timer()
        self.logger.debug("[Procesando: %s] -> DIFF=%s",
                          self.data, end - start)
        return

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
        # logger.debug(" ".join([config_name.upper(),
        # app.config.get("SQLALCHEMY_DATABASE_URI")]))

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


if __name__ == '__main__':
    server = Server(ip='0.0.0.0', port=5050)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.debug("You hit <Ctrl-C>, exiting...")
        logger.info("Closing server")
        server.server_close()
        logger.info("Server closed")
