# Standard lib imports
import logging.handlers
import os
import sys
import time
# Third Party imports
# BITSON imports

server_logger = logging.getLogger('ServerLog')
server_logger.setLevel(logging.DEBUG)

log_format = "".join(["[%(asctime)s] %(name)20s - %(levelname)8s: ",
                      "%(threadName)15s-%(funcName)15s() - %(message)s"])

formatter = logging.Formatter(fmt=log_format)
# Format UTC Time
formatter.converter = time.gmtime

# File Handler Logger
LOGDIR = os.path.join('.', 'log')
if not os.path.isdir(LOGDIR):
    os.mkdir(LOGDIR)

LOGFILE = os.path.join(
    LOGDIR,
    'server.log',
    )
fh = logging.handlers.RotatingFileHandler(filename=LOGFILE,
                                          maxBytes=10e6,
                                          backupCount=10)
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
server_logger.addHandler(fh)

# Console Handler
# if sys.stdin.isatty():
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
server_logger.addHandler(ch)


# SETTING CLIENT LOG

client_logger = logging.getLogger('ClientLog')
client_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt=log_format)
# Format UTC Time
formatter.converter = time.gmtime

# File Handler Logger
LOGDIR = os.path.join('.', 'log')
if not os.path.isdir(LOGDIR):
    os.mkdir(LOGDIR)

LOGFILE = os.path.join(
    LOGDIR,
    'client.log',
    )
fh = logging.handlers.RotatingFileHandler(filename=LOGFILE,
                                          maxBytes=10e6,
                                          backupCount=10)
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
client_logger.addHandler(fh)

# Console Handler
# if sys.stdin.isatty():
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
client_logger.addHandler(ch)