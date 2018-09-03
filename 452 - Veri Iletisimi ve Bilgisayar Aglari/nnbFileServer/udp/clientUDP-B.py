import socket
import time
import hashlib

BLOCKSIZE = 65536

UDP_IP = "127.0.0.1"
UDP_PORT = 10895

start_download_file = time.time()

file_name = ""

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.sendto("--connected--".encode(), (UDP_IP, int(UDP_PORT)))

while True:
    server_connection_response, addr = soc.recvfrom(1024)
    if "--okay--" in server_connection_response.decode("utf8"):
        file_name, addr = soc.recvfrom(1024)
        file_name = file_name.decode("utf8")
        print(file_name)
    if "--file_size_response--" in server_connection_response.decode("utf8"):
        file_size, addr = soc.recvfrom(1024)
        file_size = file_size.decode("utf8")
        bytesRemaining = int(file_size)
        print(bytesRemaining)

        file_writed = open(("../received_files/udp/" + file_name), "wb")

        while bytesRemaining != 0:
            if (bytesRemaining >= 1024):
                slab, addr = soc.recvfrom(1024)
                if "--ENDOFFILE--" in slab.decode("utf8"):
                    print("end of file")
                    break
                file_writed.write(slab)
                sizeofSlabReceived = len(slab)
                print("%d bytes are writed to file" % len(slab))
                bytesRemaining = bytesRemaining - int(sizeofSlabReceived)
                print(bytesRemaining)
            else:
                slab, addr = soc.recvfrom(bytesRemaining)
                if "--ENDOFFILE--" in slab.decode("utf8"):
                    print("end of file")
                    break
                file_writed.write(slab)
                sizeofSlabReceived = len(slab)
                print("%d bytes are writed to file" % len(slab))
                bytesRemaining = bytesRemaining - int(sizeofSlabReceived)
        print("File download completely")
        file_writed.close()
        hash_from_sender, addr = soc.recvfrom(1024)
        print("hash from sender: " + hash_from_sender.decode("utf8"))
        hasher = hashlib.md5()
        with open(("../received_files/udp/" + file_name), "rb") as file_read_check:
            buf = file_read_check.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = file_read_check.read(BLOCKSIZE)
        hash_from_calculated = hasher.hexdigest()
        print("hash from me: " + hash_from_calculated)
        if hash_from_sender.decode("utf8") == hash_from_calculated:
            print("file uploaded correctly")
        else:
            print("there is a package lose")
        end_download_file = time.time()
        total_file_download_time = end_download_file - start_download_file
        performance_file_download = open(("../performanceUDP/download/" + file_name), "a")
        performance_file_download.write(str(total_file_download_time) + "\n")
        performance_file_download.close()
        break