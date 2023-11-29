######################### server.py ########################
# # Simple server for Alice that implements a Diffie-Hellman 
# # key exchange. The server opens a socket and waits for a
# # client to connect.  Once connected Alice reicives Bob's 
# # public key and uses it to compute shared secret key.
############################################################

import socket
import pyDH
import hashlib

def encrypt(message, key):
    key_to_integer = int(key, 16)
    return message * key_to_integer

def decrypt(ciphertext, key):
    key_to_integer = int(key, 16)
    return ciphertext//key_to_integer

def alice_server():
    # read files and hash them
    hashes = []
    for i in range(1, 6):
        f = open(str(i)+".txt", "r")
        # hashes.append(hash(f.read()))
        content = f.read().encode()
        hash_value = hashlib.sha256(content).digest()
        hashes.append(int(hash_value.hex(), 16))

        print("Your file " + str(i) + " hash is " + str(hashes[i - 1]))
        # print("Your file " + str(i) + " hash is " + str(hashes[i-1]))

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

            for i in range(5):
                # Send encryption to Bob
                ciphertext = encrypt(hashes[i], alice_shared_secret)
                connection.sendall(str(ciphertext).encode())
                print("Sent ciphertext :",ciphertext)

                # Receive Encryption from Bob
                ciphertext_from_bob = int(connection.recv(1024).decode())
                print("received ciphertext:", ciphertext_from_bob)

                # Decrypt ciphertext
                message_from_bob = decrypt(ciphertext_from_bob, alice_shared_secret)
                print("H(m) from Bob:", message_from_bob)

                # Compare Hashes and see if file are equal
                if hashes[i] == message_from_bob:
                    print(f"file {i + 1} is equal")
                else:
                    print(f"file {i + 1} is not equal")


if __name__ == "__main__":
    alice_server()
