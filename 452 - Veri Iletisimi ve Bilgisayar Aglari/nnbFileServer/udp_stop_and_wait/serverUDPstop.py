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

    soc_sender.settimeout(2)
    soc_receiver.settimeout(2)

    while True:
        try:
            slab, sender_address = soc_sender.recvfrom(566)
            soc_receiver.sendto(slab, receiver_address)
            slab2, receiver_address = soc_receiver.recvfrom(566)
            soc_sender.sendto(slab2, sender_address)
        except socket.timeout:
            pass

    print("File uploaded completely")


if(__name__ == '__main__'):
    start_server()