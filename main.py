import socket
import hashlib
import pyDH         #pip install pyDH

def main():
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    A_PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
    B_PORT = 65433  # Port to listen on (non-privileged ports are > 1023)

    # Set user as default to Bob
    is_user_one = False;
    PORT = B_PORT

    # Get current user
    user = input("Are you A(lice) or B(ob)?")
    if user == 'A':
        is_user_one = True
        PORT = A_PORT

    # Get files, hash them (TODO: use multiple files)
    with open("./some_data.txt", "rb") as f:
        bytes = f.read()  # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest();
        print("Hash is:")
        print(readable_hash)

    # Get Public Key info (Group, Size, Generator)
    d1 = pyDH.DiffieHellman()

    # Use g^a or g^b to calculate H
    d1_pubkey = d1.gen_public_key()
    d1_sharedkey = None

    # Open connection with other person
    if is_user_one:
        # As Alice, create server instance
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()

            with conn:
                # Send g^a to Bob
                conn.sendall(d1_pubkey)

                # Get response Bob in form of g^b
                print(f"Connected by {addr}")
                d2 = conn.recv(1024)
                d1_sharedkey = d1.gen_shared_key(d2)

                # Print shared key
                print(d1_sharedkey)

                # TODO: Send hash of message to other person
    else:
        # As Bob, create client instance
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b"Hello, world")
            data = s.recv(1024)

main()