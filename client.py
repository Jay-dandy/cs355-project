import socket
import pyDH
import hashlib

from server import encrypt


def encrypt(message, key):
    key_to_integer = int(key, 16)
    return message * key_to_integer
def decrypt(ciphertext, key):
    key_to_integer = int(key, 16)
    return ciphertext//key_to_integer
def bob_client():
    # read files and hash them
    hashes = []
    for i in range(1, 6):
        f = open(str(i) + ".txt", "r")
        content = f.read().encode()
        hash_value = hashlib.sha256(content).digest()
        hashes.append(int(hash_value.hex(), 16))

        print("Your file " + str(i) + " hash is " + str(hashes[i - 1]))

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
        # for i in range (5):
        #     print(f"Encryption {i}: ", bob_shared_secret*hashes[i])

        for i in range(5):
            # receive ciphertext from Alice
            ciphertext_from_alice = int(s.recv(1024).decode())
            print("received ciphertext:", ciphertext_from_alice)

            # Decrypt ciphertext
            message_from_alice = decrypt(ciphertext_from_alice, bob_shared_secret)
            print("H(m) from alice:", message_from_alice)

            # Send encryption to Alice
            ciphertext = encrypt(hashes[i], bob_shared_secret)
            s.sendall(str(ciphertext).encode())
            print("Sent ciphertext :", ciphertext)

            # Compare Hashes and see if file are equal
            if hashes[i] == message_from_alice:
                print(f"file {i+1} is equal")
            else:
                print(f"file {i+1} is not equal")
if __name__ == "__main__":
    bob_client()
