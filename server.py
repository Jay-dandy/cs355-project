######################### server.py ########################
# # Simple server for Alice that implements a Diffie-Hellman 
# # key exchange. The server opens a socket and waits for a
# # client to connect.  Once connected Alice reicives Bob's 
# # public key and uses it to compute shared secret key.
############################################################

import socket
import pyDH

def alice_server():
    # read files and hash them
    hashes = []
    for i in range(1, 6):
        f = open(str(i)+".txt", "r")
        hashes.append(hash(f.read()))

        print("Your file " + str(i) + " hash is " + str(hashes[i-1]))

    # initialize DH object for Alice
    alice_dh = pyDH.DiffieHellman()
    alice_public_key = alice_dh.gen_public_key()

    # create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # bind the socket to the port
        s.bind(('localhost', 65432))
        s.listen()

        # wait for a client to connect
        print("Waiting for a connection...")
        connection, client_address = s.accept()
        with connection:
            print("Connection from", client_address)

            # send Alice's public key to Bob
            connection.sendall(str(alice_public_key).encode())

            # receive Bob's public key
            bob_public_key = int(connection.recv(1024).decode())

            # generate shared secret
            alice_shared_secret = alice_dh.gen_shared_key(bob_public_key)
            print(f"Alice's Shared Secret: {alice_shared_secret}")

if __name__ == "__main__":
    alice_server()
