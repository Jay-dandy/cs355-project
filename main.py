import socket
import hashlib
import pyDH         #pip install pyDHE

def main():
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

    # Get current user
    user = input("Are you A(lice) or B(ob)?")
    is_user_one = (user == 'A')

    # Get files, hash them (TODO: use multiple files)
    with open("./some_data.txt", "rb") as f:
        bytes = f.read()  # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest();
        print("Hash is:")
        print(readable_hash)

    d = pyDH.DiffieHellman()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)

main()