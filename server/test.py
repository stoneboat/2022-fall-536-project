NUM_OF_CLIENTS = 1000
MESSAGE_SIZE = 1460

import os;

os.system('''bash -c "time { ./server 5001 %d 2>/dev/null ; } &"''' % NUM_OF_CLIENTS)

for i in range(NUM_OF_CLIENTS):
    os.system('''bash -c "echo '%s' | ./client 127.0.0.1 5001 &"''' % (chr(65) * MESSAGE_SIZE))

os.system('''wait''')