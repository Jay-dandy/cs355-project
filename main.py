import sys
from server import alice_server
from client import bob_client

def main():
    # Ask the user to choose their role
    role = input("Choose your role (Alice or Bob): ").strip().lower()

    # Execute the corresponding function based on the user's role
    if role == 'alice':
        alice_server()
    elif role == 'bob':
        bob_client()
    else:
        print("Invalid role. Please choose either 'Alice' or 'Bob'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
