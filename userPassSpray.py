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

banners()

# Define the arguments accepted by the script
parser = argparse.ArgumentParser(description='Enumerate users on an SMTP server')
parser.add_argument('-ip', required=True, help='SMTP server IP address')
parser.add_argument('-w', required=True, help='File containing a list of usernames')
parser.add_argument('-p', help='Password to authenticate to the SMTP server (optional)')

args = parser.parse_args()

# Check if the wordlist file exists and is readable
if not os.access(args.w, os.R_OK):
    print('Could not read wordlist file:', args.w)
    sys.exit(1)

# Create a socket and connect to the SMTP server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((args.ip, 25))
except socket.error as e:
    print('Could not connect to SMTP server:', e)
    sys.exit(1)

# Receive the banner from the SMTP server
banner = s.recv(1024)
print(banner.decode())

# VRFY each user in the wordlist
with open(args.w, 'r') as f:
    for line in f:
        username = line.strip()
        # Send the VRFY command with the username
        s.send(('VRFY ' + username + '\r\n').encode())
        result = s.recv(1024).decode()
        if result.startswith('250'):
            print('User found:', username)

# If a password was provided, try to authenticate to the SMTP server
if args.p:
    s.send(('AUTH LOGIN\r\n').encode())
    result = s.recv(1024).decode()
    if result.startswith('334'):
        s.send((args.p + '\r\n').encode())
        result = s.recv(1024).decode()
        if result.startswith('235'):
            print('Authentication successful')
        else:
            print('Error authenticating:', result.strip())
            sys.exit(1)

# Close the socket
s.close()
