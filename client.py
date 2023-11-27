import socket
import pyDH

def bob_client():
    # initialize Diffie-Hellman for Bob
    bob_dh = pyDH.DiffieHellman()
    bob_public_key = bob_dh.gen_public_key()

    # create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # connecting socket to server
        s.connect(('localhost', 65432))

        # receive Alice's public key
        alice_public_key = int(s.recv(1024).decode())

        # send Bob's public key to Alice
        s.sendall(str(bob_public_key).encode())

        # generate shared secret
        bob_shared_secret = bob_dh.gen_shared_key(alice_public_key)
        print("Bob's Shared Secret:", bob_shared_secret)

if __name__ == "__main__":
    bob_client()
