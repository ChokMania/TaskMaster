import socket
import threading
from server.control_shell import ControlShell


class TaskMasterServer:
    def __init__(self, process_manager, logger, host="localhost", port=9999):
        self.process_manager = process_manager
        self.logger = logger
        self.host = host
        self.port = port
        self.control_shell = ControlShell(process_manager, logger)
        self.server_socket = None
        self.client_socket = None

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        self.logger.info(f"TaskMaster server listening on {self.host}:{self.port}")

        while True:
            client_socket, addr = self.server_socket.accept()
            self.logger.info(f"Accepted connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        try:
            client_addr = client_socket.getpeername()
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                command = data.decode().strip()
                self.logger.info(f"Received command: {command}")
                response = self.control_shell.onecmd(command)
                if response is not None:
                    client_socket.sendall(response.encode())
        finally:
            client_socket.close()
            self.logger.info(f"Closed connection to {client_addr}")
