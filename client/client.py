import socket
import argparse


def client():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--host", type=str, default="localhost", help="TaskMaster server host"
        )
        parser.add_argument("--port", type=int, default=9001, help="TaskMaster server port")
        args = parser.parse_args()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((args.host, args.port))
            print("Connected to TaskMaster server")

            while True:
                user_input = input("(taskmaster) ")
                s.sendall(user_input.encode())
                data = s.recv(1024)
                print(data.decode())
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    client()
