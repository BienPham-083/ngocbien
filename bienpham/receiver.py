import socket
import hashlib
import os

SAVE_FOLDER = 'received'
os.makedirs(SAVE_FOLDER, exist_ok=True)

def start_receiver(host='0.0.0.0', port=9999):
    s = socket.socket()
    s.bind((host, port))
    s.listen(1)

    print(f"Receiver listening on {host}:{port}...")

    while True:
        conn, addr = s.accept()
        print(f"🔌 Connection from {addr}")

        received = b""
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            received += chunk
        conn.close()

        try:
            hash_received, file_data = received.split(b'\n', 1)
        except ValueError:
            print("❌ Invalid format received!")
            continue

        hash_calculated = hashlib.sha256(file_data).hexdigest().encode()

        if hash_received == hash_calculated:
            save_path = os.path.join(SAVE_FOLDER, 'received_file.txt')
            with open(save_path, 'wb') as f:
                f.write(file_data)
            print("✅ File received and verified successfully.")
        else:
            print("❌ Hash mismatch! File may be corrupted.")

if __name__ == "__main__":
    start_receiver()
