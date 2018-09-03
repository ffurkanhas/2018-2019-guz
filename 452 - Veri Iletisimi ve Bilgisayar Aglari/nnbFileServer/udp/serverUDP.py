import sys
import socket

host = '127.0.0.1'
server_port_sender = 16796
server_port_receiver = 10895

soc_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc_receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def start_server():
    print('Socket created')
    try:
        soc_sender.bind((host, server_port_sender))
        soc_receiver.bind((host, server_port_receiver))
        print('Socket bind complete')
    except socket.error as msg:
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()
    print('Socket now listening')
    accept_message_from_sender, sender_address = soc_sender.recvfrom(1024)
    accept_message_from_receiver, receiver_address = soc_receiver.recvfrom(1024)

    accept_message_from_sender = accept_message_from_sender.decode("utf8").rstrip()
    accept_message_from_receiver = accept_message_from_receiver.decode("utf8").rstrip()
    print(accept_message_from_receiver)
    print(accept_message_from_sender)

    if accept_message_from_sender == "--connected--" and accept_message_from_receiver == "--connected--":
        print("clients connected")

    soc_sender.sendto("--okay--".encode(), sender_address)
    soc_receiver.sendto("--okay--".encode(), receiver_address)

    file_name_from_sender, sender_address = soc_sender.recvfrom(1024)
    file_name_from_sender = file_name_from_sender.decode("utf8")
    print(file_name_from_sender)

    soc_receiver.sendto(file_name_from_sender.encode(), receiver_address)

    soc_sender.sendto("--file_size_request--".encode(), sender_address)

    file_size_from_sender, sender_address = soc_sender.recvfrom(1024)
    print(file_size_from_sender.decode("utf8"))

    bytesRemaining = int(file_size_from_sender.decode("utf8"))

    soc_receiver.sendto("--file_size_response--".encode(), receiver_address)

    soc_receiver.sendto(file_size_from_sender, receiver_address)

    while bytesRemaining != 0:
        if (bytesRemaining >= 1024):
            slab, sender_address = soc_sender.recvfrom(1024)
            if "--ENDOFFILE--" in slab.decode("utf8"):
                soc_receiver.sendto("--ENDOFFILE--".encode(), receiver_address)
                print("end of file")
                break
            sizeofSlabReceived = len(slab)
            soc_receiver.sendto(slab, receiver_address)
            print("%d bytes received and forwarded to client B ok" % len(slab))

            bytesRemaining = bytesRemaining - int(sizeofSlabReceived)
            print("remaining: " + str(bytesRemaining))
        else:
            slab, sender_address = soc_sender.recvfrom(bytesRemaining)
            if "--ENDOFFILE--" in slab.decode("utf8"):
                soc_receiver.sendto("--ENDOFFILE--".encode(), receiver_address)
                print("end of file")
                break
            sizeofSlabReceived = len(slab)
            soc_receiver.sendto(slab, receiver_address)
            print("%d bytes received and forwarded to client B" % len(slab))
            bytesRemaining = bytesRemaining - int(sizeofSlabReceived)
            print("remaining: " + str(bytesRemaining))
    while True:
        soc_sender.sendto("--end--".encode(), sender_address)
        sender_okay, sender_address = soc_sender.recvfrom(1024)
        if "--end_okay--" in sender_okay.decode("utf8"):
            break
    print("File uploaded completely")
    hash_from_sender, sender_address = soc_sender.recvfrom(1024)
    soc_receiver.sendto(hash_from_sender, receiver_address)
    print("hash from sender forwarded to receiver: " + hash_from_sender.decode("utf8"))


if(__name__ == '__main__'):
    start_server()