import sys
import socket
from threading import Thread

host = '127.0.0.1'
server_port = 16796
connection_list = [] #first one is sender, second one is receiver

def client_thread(conn, ip, port):
    still_listen = True
    while still_listen:
        input_from_client = conn.recv(1024).decode("utf8").rstrip()

        if "--ENDOFDATA--" in input_from_client:
            print('--ENDOFDATA--')
            conn.close()
            print('Connection from ' + ip + ':' + port + " ended")
            still_listen = False
        else:
            if (input_from_client is "s"): #give file from the client <--- client a
                while len(connection_list) < 2:
                    conn.sendall("--wait--".encode())
                conn.sendall("--okay--".encode())
                fileName = conn.recv(1024).decode("utf8").rstrip()
                print('User: ' + str(ip) + ':' + str(port) + ' will send: %s' % fileName)

                connection_list[1].sendall(str(fileName).encode()) #send file name to client B

                conn.sendall("--okay--".encode())

                fileSize = conn.recv(1024).decode("utf8").rstrip()
                print("File size: %s" % fileSize)

                connection_list[1].sendall(str(fileSize).encode()) #send file size to client B

                bytesRemaining = int(fileSize)
                while bytesRemaining != 0:
                    if (bytesRemaining >= 1024):
                        slab = conn.recv(1024)
                        connection_list[1].sendall(slab)
                        sizeofSlabReceived = len(slab)
                        print("%d bytes received and forwarded to client B" % len(slab))
                        bytesRemaining = bytesRemaining - int(sizeofSlabReceived)
                    else:
                        slab = conn.recv(bytesRemaining)  # of 1024
                        connection_list[1].sendall(slab)
                        sizeofSlabReceived = len(slab)
                        print("%d bytes received and forwarded to client B" % len(slab))
                        bytesRemaining = bytesRemaining - int(sizeofSlabReceived)
                print("File uploaded completely")

                file_hash = conn.recv(32).decode("utf8").rstrip() #receive file hash from client a
                print(file_hash)
                connection_list[1].sendall(str(file_hash).encode()) #send file hash to client a

def start_server():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # if there is an error close the sockets
    print('Socket created')
    try:
        soc.bind((host, server_port))
        print('Socket bind complete')
    except socket.error as msg:
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    soc.listen(2)
    print('Socket now listening')

    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Accepting connection from ' + ip + ':' + port)
        connection_list.append(conn)
        try:
            Thread(target=client_thread, args=(conn, ip, port)).start()
        except:
            print("Terible error!")
            import traceback
            traceback.print_exc()
    soc.close()

if(__name__ == '__main__'):
    start_server()