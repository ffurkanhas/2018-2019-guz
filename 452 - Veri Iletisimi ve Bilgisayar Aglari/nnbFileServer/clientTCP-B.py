import socket
import hashlib
import time

BLOCKSIZE = 65536

path = ("./")
received_path = ("./received_files/")

start_download_file = time.time()

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 16796
soc.connect((host, port))
sender_or_receiver = 'r'
soc.send(sender_or_receiver.encode())

print("connected")

file_name = soc.recv(1024).decode("utf8").rstrip()

file_size = soc.recv(1024).decode("utf8").rstrip()
print(str(file_name) + " will downloaded " + str(file_size))

file_writed = open((received_path + file_name), "wb")
bytesRemaining = int(file_size)

while bytesRemaining != 0:
    if (bytesRemaining >= 1024):
        slab = soc.recv(1024)
        file_writed.write(slab)
        sizeofSlabReceived = len(slab)
        print("%d bytes are writed to file" % len(slab))

        bytesRemaining = bytesRemaining - int(sizeofSlabReceived)
    else:
        slab = soc.recv(bytesRemaining)
        file_writed.write(slab)
        sizeofSlabReceived = len(slab)
        print("%d bytes are writed to file" % len(slab))
        bytesRemaining = bytesRemaining - int(sizeofSlabReceived)
print("File download completely")
file_writed.close()
file_hash_given = soc.recv(32).decode("utf8").rstrip()
print("file hash from client a: " + file_hash_given)
hasher2 = hashlib.md5()
with open((received_path + file_name), "rb") as file_writed_check:
    buf = file_writed_check.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher2.update(buf)
        buf = file_writed_check.read(BLOCKSIZE)
file_hash = hasher2.hexdigest()
print("file hash created by me: " + file_hash)
file_corretness_flag = False
if file_hash_given == file_hash:
    print("file is correct")
    file_corretness_flag = True
else:
    print("file is not correct")

soc.sendall('--ENDOFDATA--'.encode())
end_download_file = time.time()
total_file_download_time = end_download_file - start_download_file
print("Total time for download file: " + str(total_file_download_time))
performance_file_download = open((path + "performanceTCP/download/" + file_name[:str(file_name).index(".")] + ".txt"), "a")
performance_file_download.write(str(total_file_download_time) + " " + str(file_corretness_flag) + "\n")
performance_file_download.close()
