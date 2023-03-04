import argparse
import socket
import sys
import os

def banners():
    print("""
    *********************************************
        SMTP Enum Tool VRFY method + PassSpray
        Author: sergiovks
    *********************************************
    """)

def vrfy(ip, wordlist, timeout):
    # Check if the wordlist file exists and is readable
    if not os.access(wordlist, os.R_OK):
        print('Could not read wordlist file:', wordlist)
        sys.exit(1)

    # Create a socket and set timeout
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    # Connect to the SMTP server
    try:
        s.connect((ip, 25))
    except socket.error as e:
        print('Could not connect to SMTP server:', e)
        sys.exit(1)

    # Receive the banner from the SMTP server
    banner = s.recv(1024)
    print(banner.decode())

    # VRFY each user in the wordlist
    with open(wordlist, 'r') as f:
        for line in f:
            username = line.strip()
            # Send the VRFY command with the username
            s.send(('VRFY ' + username + '\r\n').encode())
            result = s.recv(1024).decode()
            if result.startswith('250'):
                print('User found:', username)

    # Close the socket
    s.close()

def main():
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description='Enumerate users on an SMTP server')
    parser.add_argument('-ip', required=True, help='SMTP server IP address')
    parser.add_argument('-w', '--wordlist', required=True, help='File containing a list of usernames')
    parser.add_argument('-p', '--password', help='Password to authenticate to the SMTP server (optional)')
    parser.add_argument('-t', '--timeout', type=int, default=5, help='Timeout in seconds (default: 5)')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()

    # Display the banner
    banners()

    # Call the VRFY function with the provided arguments
    vrfy(args.ip, args.wordlist, args.timeout)

    # If a password was provided, try to authenticate to the SMTP server
    if args.password:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((args.ip, 25))
        s.send(('AUTH LOGIN\r\n').encode())
        result = s.recv(1024).decode()
        if result.startswith('334'):
            s.send((args.password + '\r\n').encode())
            result = s.recv(1024).decode()
            if result.startswith('235'):
                print('Authentication successful')
            else:
                print('Error authenticating:', result.strip())
                sys.exit(1)
        s.close()

if __name__ == '__main__':
    main()
