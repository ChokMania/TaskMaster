import socket
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str, help="Command to send to the TaskMaster server")
    parser.add_argument("--host", type=str, default="localhost", help="TaskMaster server host")
    parser.add_argument("--port", type=int, default=9999, help="TaskMaster server port")
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((args.host, args.port))
        s.sendall(args.command.encode())
        data = s.recv(1024)

    print("Received", repr(data))


if __name__ == "__main__":
    main()