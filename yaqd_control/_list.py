import json
import socket
from pprint import pprint


def list_(host="127.0.0.1", start=36000, stop=39999):
    for i in range(start, stop + 1):
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
