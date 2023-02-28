import socket
import sys

if len(sys.argv) == 2 and sys.argv[1] == '-h':
  print("Usage: vrfy.py -ip SMTP_IP -w WORDLIST_FILE")
  sys.exit(0)

if len(sys.argv) != 4 or sys.argv[1] != '-ip':
  print("Usage: vrfy.py -ip SMTP_IP -w WORDLIST_FILE")
  sys.exit(0)
  
#Create a Socket and connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect = s.connect((sys.argv[2],25))

#Receive the banner
banner = s.recv(1024)
print(banner)

#Read usernames from wordlist file
with open(sys.argv[3], 'r') as f:
    for line in f:
        #VRFY each username
        s.send('VRFY ' + line.strip() + '\r\n')
        result = s.recv(1024)
        print(result)

#Close the socket
s.close()
