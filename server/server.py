import socket
import threading
from server.control_shell import ControlShell


class TaskMasterServer:
    def __init__(self, process_manager, logger, host="localhost", port=9001):
        self.process_manager = process_manager
        self.logger = logger
        self.host = host
        self.port = port
        self.control_shell = ControlShell(process_manager=process_manager, logger=logger, server=self)
        self.server_socket = None
        self.client_socket = None
        self.is_running = True

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        self.logger.info(f"TaskMaster server listening on {self.host}:{self.port}")

        while self.is_running:
            client_socket, addr = self.server_socket.accept()
            self.logger.info(f"Accepted connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def stop(self):
        self.is_running = False
        if self.server_socket is not None:
            self.server_socket.shutdown(socket.SHUT_RDWR)
            self.server_socket.close()
            self.logger.info("TaskMaster server stopped.")

    def handle_client(self, client_socket):
        try:
            client_addr = client_socket.getpeername()
            while self.is_running:
                data = client_socket.recv(1024)
                if not data:
                    break
                command = data.decode().strip()
                self.logger.info(f"Received command: {command}")
                response = self.control_shell.onecmd(command)
                print("response = ", response)
                if response is not None:
                    client_socket.sendall(response.encode())
        finally:
            client_socket.close()
            self.logger.info(f"Closed connection to {client_addr}")
