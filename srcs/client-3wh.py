#!/usr/bin/env python

from scapy.all import *
import threading

import logging
logger = logging.getLogger(__name__)

SEND_PACKET_SIZE = 1000  # should be less than max packet size of 1500 bytes

# A client class for implementing TCP's three-way-handshake connection establishment and closing protocol,
# along with data transmission.

#   Name: Yu Wei, Zhongtang Luo
#   PUID: 33702049, 32759316


class Client3WH:

    def __init__(self, dip, dport):
        """Initializing variables"""
        self.dip = dip
        self.dport = dport
        # selecting a source port at random
        self.sport = random.randrange(0, 2**16)

        self.next_seq = 0                       # TCP's next sequence number
        self.next_ack = 0                       # TCP's next acknowledgement number

        self.ip = IP(dst=self.dip)              # IP header
        self.tcp = self.ip/TCP(sport=self.sport, dport=self.dport, flags=0, seq=self.next_seq) # TCP header

        self.connected = False
        self.timeout = 3

    def _start_sniffer(self):
        t = threading.Thread(target=self._sniffer)
        t.start()

    def _filter(self, pkt):
        if (IP in pkt) and (TCP in pkt):  # capture only IP and TCP packets
            if (pkt[TCP].dport == self.sport): # capture only incoming packets
                return True
        return False

    def _sniffer(self):
        while self.connected:
            sniff(prn=lambda x: self._handle_packet(
                x), lfilter=lambda x: self._filter(x), count=1, timeout=self.timeout)

    def _handle_packet(self, pkt):
        """TODO(1): Handle incoming packets from the server and acknowledge them accordingly. Here are some pointers on
           what you need to do:
           1. If the incoming packet has data (or payload), send an acknowledgement (TCP) packet with correct 
              `sequence` and `acknowledgement` numbers.
           2. If the incoming packet is a FIN (or FINACK) packet, send an appropriate acknowledgement or FINACK packet
              to the server with correct `sequence` and `acknowledgement` numbers.
        """

        ### BEGIN: ADD YOUR CODE HERE ... ###
        if pkt[TCP].flags & 0x3f == 0x01:     # FIN
            logger.debug("sub Thread RCV: FIN with Seq {}".format(pkt[TCP].seq))
            self.tcp[TCP].flags = "FA"
            self.tcp[TCP].ack = pkt[TCP].seq + 1
            self.next_seq = self.tcp[TCP].seq + 1
            logger.debug("sub Thread SND: FIN -> FIN+ACK with ACK {}, Seq {}".format(self.tcp[TCP].ack, self.tcp[TCP].seq))
            send(self.tcp)
            self.tcp[TCP].seq = self.next_seq
        elif pkt[TCP].flags & 0x3f == 0x11:     # FIN+ACK
            logger.debug("sub Thread RCV: FIN+ACK with ACK {}, Seq {}".format(pkt[TCP].ack, pkt[TCP].seq))
            self.tcp[TCP].flags = "A"
            self.tcp[TCP].ack = pkt[TCP].seq + 1
            send(self.tcp)
            logger.debug("sub Thread SND: FIN+ACK -> ACK with ACK {}, Seq {}".format(self.tcp[TCP].ack, self.tcp[TCP].seq))
        elif pkt[TCP].flags & 0x3f == 0x04:  #RST
            logger.debug("sub Thread RCV: RST")
            logger.error("sub Thread ERR: RST")
            exit
        elif pkt[TCP].flags & 0x3f == 0x18:  #PA
            logger.debug("sub Thread RCV: PA with Seq {}".format(pkt[TCP].seq))
            self.tcp[TCP].ack = pkt[TCP].seq + len(pkt.payload)
            logger.debug("sub Thread SND: PA -> ACK with ACK {}, Seq {}".format(self.tcp[TCP].ack, self.tcp[TCP].seq))
        ### END: ADD YOUR CODE HERE ... #####

    def connect(self):
        """TODO(2): Implement TCP's three-way-handshake protocol for establishing a connection. Here are some
           pointers on what you need to do:
           1. Handle SYN -> SYNACK -> ACK packets.
           2. Make sure to update the `sequence` and `acknowledgement` numbers correctly, along with the 
              TCP `flags`.
        """

        ### BEGIN: ADD YOUR CODE HERE ... ###
        # send SYN  
        logger.debug("SND: SYN with Seq {} ".format(self.tcp[TCP].seq))
        self.tcp[TCP].flags = "S"
        self.next_seq = self.tcp[TCP].seq + 1
        pkt = sr1(self.tcp, timeout=self.timeout)

        assert pkt is not None, "ERR in connection phase: no packet received"
        assert pkt[TCP].flags & 0x3f == 0x12, "ERR in connection phase: packet type does not match"
        logger.debug("RCV: SYN+ACK with ACK {}, Seq {}".format(pkt[TCP].ack, pkt[TCP].seq))
        self.tcp[TCP].seq = self.next_seq

        # send SA ACK
        self.tcp[TCP].ack = pkt[TCP].seq+1
        self.tcp[TCP].flags = "A"
        logger.debug("SND: SYN+ACK -> ACK with ACK {}, Seq {}".format(self.tcp[TCP].ack, self.tcp[TCP].seq))

        send(self.tcp)  
        self.tcp[TCP].seq = self.next_seq
        ### END: ADD YOUR CODE HERE ... #####

        self.connected = True
        self._start_sniffer()
        print('Connection Established')
    def close(self):
        """TODO(3): Implement TCP's three-way-handshake protocol for closing a connection. Here are some
           pointers on what you need to do:
           1. Handle FIN -> FINACK -> ACK packets.
           2. Make sure to update the `sequence` and `acknowledgement` numbers correctly, along with the 
              TCP `flags`.
        """

        ### BEGIN: ADD YOUR CODE HERE ... ###
        # send FIN
        logger.debug("SND: FIN with ACK {}, Seq {}".format(self.tcp[TCP].ack, self.tcp[TCP].seq))
        self.next_seq = self.tcp[TCP].seq + 1
        self.tcp[TCP].flags = "FA"
        pkt = sr1(self.tcp, timeout=self.timeout)
        self.tcp[TCP].seq = self.next_seq

        assert pkt is not None, "ERR in close phase: no packet received"
        assert pkt[TCP].flags & 0x3f == 0x11, "ERR in close phase: packet type does not match"
        logger.debug("RCV: FIN+ACK with ACK {}, Seq {}".format(pkt[TCP].ack, pkt[TCP].seq))
        self.tcp[TCP].flags = "A"
        self.tcp[TCP].ack = pkt[TCP].seq + 1
        self.next_seq = self.tcp[TCP].seq + 1
        send(self.tcp)
        logger.debug("SND: FIN+ACK -> ACK with ACK {}, Seq {}".format(self.tcp[TCP].ack, self.tcp[TCP].seq))
        self.tcp[TCP].seq = self.next_seq
        ### END: ADD YOUR CODE HERE ... #####

        self.connected = False
        print('Connection Closed')

    def send(self, payload):
        """TODO(4): Create and send TCP's data packets for sharing the given message (or file):
           1. Make sure to update the `sequence` and `acknowledgement` numbers correctly, along with the 
              TCP `flags`.
        """

        ### BEGIN: ADD YOUR CODE HERE ... ###
        logger.debug("SND: PA with Seq {} ".format(self.tcp[TCP].seq))
        self.tcp[TCP].flags = "PA"
        self.next_seq = self.tcp[TCP].seq + len(payload)
        pkt = sr1(self.tcp/payload, timeout=self.timeout)

        assert pkt is not None, "ERR in data sending phase: no packet received"
        assert pkt[TCP].flags & 0x3f == 0x10, "ERR in data sending phase: packet typ does not match"
        assert pkt[TCP].ack == self.next_seq, "ERR in data sending phase: ack number does not match"
        logger.debug("RCV: A with ACK {}, Seq {}".format(pkt[TCP].ack, pkt[TCP].seq))

        self.tcp[TCP].seq = self.next_seq
        ### END: ADD YOUR CODE HERE ... #####


def main():
    """Parse command-line arguments and call client function """
    if len(sys.argv) != 3:
        sys.exit(
            "Usage: ./client-3wh.py [Server IP] [Server Port] < [message]")
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.ERROR)

    client = Client3WH(server_ip, server_port)
    client.connect()

    message = sys.stdin.read(SEND_PACKET_SIZE)
    while message:
        client.send(message)
        message = sys.stdin.read(SEND_PACKET_SIZE)

    client.close()


if __name__ == "__main__":
    main()

