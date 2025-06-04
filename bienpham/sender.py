import socket
import hashlib

def send_file(file_path, host='localhost', port=9999):
    s = socket.socket()
    s.connect((host, port))

    with open(file_path, 'rb') as f:
        data = f.read()

    hash_value = hashlib.sha256(data).hexdigest()
    s.sendall(hash_value.encode() + b'\n' + data)
    s.close()
