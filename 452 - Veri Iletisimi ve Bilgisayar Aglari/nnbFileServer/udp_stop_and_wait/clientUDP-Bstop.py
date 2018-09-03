import socket
import time
import hashlib
import base64

BLOCKSIZE = 65536

splitter = "|ben|an|"

UDP_IP = "127.0.0.1"
UDP_PORT = 10895

file_name = "1.txt"

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.sendto("--connected--".encode(), (UDP_IP, int(UDP_PORT)))

while True:
    server_connection_response, addr = soc.recvfrom(1024)
    while "--okay--" not in server_connection_response.decode("utf8"):
        server_connection_response, addr = soc.recvfrom(1024)

    file_writed = open(("../received_files/udpStopAndWait/" + file_name), "wb")

    seqNoFlag = 0
    connection_trials_count = 0
    soc.settimeout(1)

    start_download_file = time.time()
    bit_error_trials_count = 0
    while 1:
        print('Wait...')
        try:
            data, server = soc.recvfrom(4096)
            connection_trials_count = 0
        except:
            continue
        seqNo = data.split(b'|ben|an|')[1].decode()
        print(str(seqNo))

        clientHash = hashlib.md5(data.split(b'|ben|an|')[3]).hexdigest()
        print("Server hash: " + data.split(b'|ben|an|')[0].decode())
        print("Client hash: " + clientHash)
        if data.split(b'|ben|an|')[0].decode() == clientHash and seqNoFlag == int(seqNo == True):
            packetLength = data.split(b'|ben|an|')[2].decode()
            file_writed.write(data.split(b'|ben|an|')[3])
            print("Sequence number: " + str(seqNo))

            sent = soc.sendto((str(seqNo) + "," + str(packetLength)).encode(), server)
            bit_error_trials_count = 0
        else:
            print("esit degil")
            if bit_error_trials_count < 1:
                bit_error_trials_count += 1
                continue
            else:
                print("ok")
                packetLength = data.split(b'|ben|an|')[2].decode()
                sent = soc.sendto((str(seqNo) + "," + str(packetLength)).encode(), server)
                bit_error_trials_count = 0
        if int(packetLength) < 500:
            seqNo = int(not seqNo)
            break

    print("File download completely")
    file_writed.close()
    end_download_file = time.time()
    total_file_download_time = end_download_file - start_download_file
    performance_file_download = open(("../performanceUDPStopAndWait/download/" + file_name), "a")
    performance_file_download.write(str(total_file_download_time) + "\n")
    performance_file_download.close()
    break