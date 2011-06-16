# -*- coding: utf-8 -*-

import logging
import socket

from pelita.messaging.remote import TcpSocket
from pelita.messaging.utils import SuspendableThread

_logger = logging.getLogger("pelita.listener")

class TcpListeningSocket(TcpSocket):
    def __init__(self, host, port):
        """ Opens a socket with respective host and port
        and listens for an incoming connection.
        """

        super(TcpListeningSocket, self).__init__(host, port)

        self.socket.bind( (self.host, self.port) )
        self.socket.listen(1)

    def handle_accept(self):
        """ Waits for a connection to be established and returns it."""
        connection, addr = self.socket.accept()
        _logger.info("Connection accepted.")

        return connection

class TcpThreadedListeningServer(SuspendableThread):
    def __init__(self, host, port):
        """ Opens a socket with respective host and port
        and listens for an incoming connection.

        Each instantiation must supply its own on_accept()
        method which specifies what action needs to be done
        when a new connection is established.
        """
        SuspendableThread.__init__(self)

        self.socket = TcpListeningSocket(host, port)

        # if there is a problem with closing, enable the timeout
        # self.socket.timeout = 3

    def run(self):
        while self._running:
            try:
                connection = self.socket.handle_accept()

                # we waited so long, we need to see that we're still alive
                # if it was a dummy connection, we will return now
                if not self._running:
                    return

                # okay, we are alive (unless, of course, we died in between)
                # handle the new connection
                self.on_accept(connection)

            except socket.timeout as e:
                _logger.debug("socket.timeout: %s" % e)
                continue

            except Exception as e:
                _logger.exception(e)
                continue

    def on_accept(self, connection):
        raise NotImplementedError

    def stop(self):
        SuspendableThread.stop(self)

        # To stop listening, we create a dummy connection
        # and close it immediately
        dummy = socket.socket()
        dummy.connect((self.socket.host, self.socket.port))
        dummy.close()

class TcpThreadedListeningServerQueuer(TcpThreadedListeningServer):
    def __init__(self, incoming_connections, host, port):
        TcpThreadedListeningServer.__init__(self, host, port)

        self.incoming_connections = incoming_connections

    def on_accept(self, connection):
        self.incoming_connections.put(connection)


