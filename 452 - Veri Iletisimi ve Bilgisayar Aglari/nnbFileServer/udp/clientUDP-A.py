import socket
import os
import time
import hashlib
import sys

BLOCKSIZE = 65536

UDP_IP = "127.0.0.1"
UDP_PORT = 16796

fileName = "10.txt"

start_upload_file = time.time()

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.sendto("--connected--".encode(), (UDP_IP, int(UDP_PORT)))

while True:
    server_connection_response, addr = soc.recvfrom(1024)
    if "--okay--" in server_connection_response.decode("utf8"):
        file_name = fileName
        soc.sendto(file_name.encode(), (UDP_IP, int(UDP_PORT)))
    if "--file_size_request--" in server_connection_response.decode("utf8"):
        file_size = os.path.getsize("../" + fileName)
        soc.sendto(str(file_size).encode(), (UDP_IP, int(UDP_PORT)))

        f = open(("../" + fileName), "rb")
        buffRead = 0
        bytesRemaining = int(file_size)

        while bytesRemaining != 0:
            if (bytesRemaining >= 1024):
                buffRead = f.read(1024)
                sizeofSlabRead = len(buffRead)
                print('remaining: %d' % bytesRemaining)
                print('read: %d' % sizeofSlabRead)
                soc.sendto(buffRead, (UDP_IP, int(UDP_PORT)))
                bytesRemaining = bytesRemaining - int(sizeofSlabRead)
            else:
                buffRead = f.read(bytesRemaining)
                sizeofSlabRead = len(buffRead)
                print('remaining: %d' % bytesRemaining)
                print('read: %d' % sizeofSlabRead)
                soc.sendto(buffRead, (UDP_IP, int(UDP_PORT)))
                bytesRemaining = bytesRemaining - int(sizeofSlabRead)
        print("Read file completely")
        f.close()
        while True:
            soc.sendto("--ENDOFFILE--".encode(), (UDP_IP, int(UDP_PORT)))
            server_end_response, addr = soc.recvfrom(1024)
            if "--end--" in server_end_response.decode("utf8"):
                soc.sendto("--end_okay--".encode(), (UDP_IP, int(UDP_PORT)))
                break
        hasher = hashlib.md5()
        with open(("../" + fileName), "rb") as file_read_check:
            buf = file_read_check.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = file_read_check.read(BLOCKSIZE)
        soc.sendto(hasher.hexdigest().encode(), (UDP_IP, int(UDP_PORT)))
        print(hasher.hexdigest())
        end_upload_file = time.time()
        total_file_upload_time = end_upload_file - start_upload_file
        performance_file_upload = open(("../performanceUDP/upload/" + fileName), "a")
        performance_file_upload.write(str(total_file_upload_time) + "\n")
        performance_file_upload.close()
        break