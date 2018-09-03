import socket
import time
import hashlib

BLOCKSIZE = 65536

splitter = "|ben|an|"

class veri():
    checksum = 0
    length = 0
    seqNo = 0
    msg = 0

    def make(self, data):
        self.msg = data
        self.length = str(len(data))
        self.checksum=hashlib.md5(data.encode()).hexdigest()

UDP_IP = "127.0.0.1"
UDP_PORT = 16796

fileName = "1.txt"

start_upload_file = time.time()

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.sendto("--connected--".encode(), (UDP_IP, int(UDP_PORT)))

while True:
    server_connection_response, addr = soc.recvfrom(1024)
    while "--okay--" not in server_connection_response.decode("utf8"):
        server_connection_response, addr = soc.recvfrom(1024)

    f = open(("../" + fileName), "rb")
    buffRead = 0
    sequence_number = 0
    file_data = f.read()
    f.close()

    pkt = veri()

    packet_count = 0

    x = 0
    while x < int((len(file_data) / 500) + 1):
        packet_count += 1
        msg = file_data[x * 500:x * 500 + 500]
        pkt.make(msg.decode())
        finalPacket = str(pkt.checksum) + splitter + str(pkt.seqNo) + splitter + str(pkt.length) + splitter + str(pkt.msg)

        sent = soc.sendto(finalPacket.encode(), (UDP_IP, int(UDP_PORT)))

        print('Sent ' + str(sent) + ' bytes back.')
        soc.settimeout(2)

        try:
            ack, address = soc.recvfrom(100)
            ack = ack.decode()
        except:
            print("Time out")
            continue
        if ack.split(",")[0] == str(pkt.seqNo):
            pkt.seqNo = int(not pkt.seqNo)
            print("Ack: " + ack)
            x += 1
            print(str(x))
            print("***" + str((len(file_data) / 500) + 1))

    print("Read file completely")
    end_upload_file = time.time()
    total_file_upload_time = end_upload_file - start_upload_file
    performance_file_upload = open(("../performanceUDPStopAndWait/upload/" + fileName), "a")
    performance_file_upload.write(str(total_file_upload_time) + "\n")
    performance_file_upload.close()
    break