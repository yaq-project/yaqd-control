import argparse
import json
import socket
from pprint import pprint

def main():
    parser = argparse.ArgumentParser(description="List open yaq daemon ports")
    parser.add_argument("host", nargs="?", default="127.0.0.1")
    parser.add_argument("--start", "-s", type=int, default=36000, help="start scanning at port")
    parser.add_argument("--stop", "-S", type=int, default=39999, help="stop scanning at port")
    args = parser.parse_args()
    host = args.host 
    for i in range(args.start, args.stop + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((host, i))
            s.sendall(b'{"jsonrpc":"2.0", "method": "id", "id":"find"}')
            ident = json.loads(s.recv(1024))
        except Exception as e:
            continue
        print(f"Port: {i}")
        pprint(ident["result"])
        s.close()

if __name__ == "__main__":
    main()
