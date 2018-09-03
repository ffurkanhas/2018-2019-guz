import socket
import os
import hashlib
import time

BLOCKSIZE = 65536

path = ("./")

start_upload_file = time.time()

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 16796
soc.connect((host, port))
sender_or_receiver = 's'
soc.send(sender_or_receiver.encode())

server_connection_response, addr = soc.recvfrom(1024)
while "--okay--" not in server_connection_response.decode("utf8"):
    server_connection_response, addr = soc.recvfrom(1024)

print("connected")

file_name = "10.txt"
soc.send(file_name.encode())

fileSize = os.path.getsize(file_name)
soc.sendall(str(fileSize).encode())

server_connection_response, addr = soc.recvfrom(1024)
while "--okay--" not in server_connection_response.decode("utf8"):
    server_connection_response, addr = soc.recvfrom(1024)

f = open((path + file_name), "rb")
buffRead = 0
bytesRemaining = int(fileSize)

while bytesRemaining != 0:
    if (bytesRemaining >= 1024):
        buffRead = f.read(1024)
        sizeofSlabRead = len(buffRead)
        print('remaining: %d' % bytesRemaining)
        print('read: %d' % sizeofSlabRead)
        soc.sendto(buffRead, (host, port))
        bytesRemaining = bytesRemaining - int(sizeofSlabRead)
    else:
        buffRead = f.read(bytesRemaining)
        sizeofSlabRead = len(buffRead)
        print('remaining: %d' % bytesRemaining)
        print('read: %d' % sizeofSlabRead)
        soc.sendto(buffRead, (host, port))
        bytesRemaining = bytesRemaining - int(sizeofSlabRead)
print("Read file completely")
f.close()
hasher = hashlib.md5()
with open((path + file_name), "rb") as file_read_check:
    buf = file_read_check.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher.update(buf)
        buf = file_read_check.read(BLOCKSIZE)
soc.send(hasher.hexdigest().encode())
soc.sendall('--ENDOFDATA--'.encode())
end_upload_file = time.time()
total_file_upload_time = end_upload_file - start_upload_file
print("Total time for upload file: " + str(total_file_upload_time))
performance_file_upload = open((path + "performanceTCP/upload/" + file_name), "a")
performance_file_upload.write(str(total_file_upload_time) + "\n")
performance_file_upload.close()