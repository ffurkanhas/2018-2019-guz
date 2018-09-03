import sys
import socket
import random

host = '127.0.0.1'
server_port_sender = 16796
server_port_receiver = 10895

loseFile = open("loseFile.txt", 'r')

line = loseFile.read()
package_lose_rate = line[:line.index(":")]
bit_error_rate = line[line.index(":") + 1:]

package_lose_rate_number = float(package_lose_rate.replace(",", "."))
bit_error_rate_number = float(bit_error_rate.replace(",", "."))

print("p: " + str(package_lose_rate_number) + "\nq: " + str(bit_error_rate_number))

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
            random_number_for_package = random.random()
            slab, sender_address = soc_sender.recvfrom(566)

            if package_lose_rate_number < random_number_for_package:
                print("normal")
                soc_receiver.sendto(slab, receiver_address)
            else:
                print("bit error")
                slabString = slab.decode()
                slabChangedBits = changeBits(slabString, int(bit_error_rate_number * 10))
                slabWillSent = frombits(slabChangedBits)
                slabSender = slabWillSent.encode()
                soc_receiver.sendto(slabSender, receiver_address)

            slab2, receiver_address = soc_receiver.recvfrom(566)
            soc_sender.sendto(slab2, sender_address)
        except socket.timeout:
            pass

    print("File uploaded completely")

def changeBits(s, rate):
    result = []
    rate = int(rate)
    i = 0
    for c in s:
        bits = bin(ord(c))[2:]
        if i < rate:
            bits = '00000001'[len(bits):] + bits
            i += 1
        else:
            bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def frombits(bits):
    chars = []
    for b in range(int(len(bits) / 8)):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


if(__name__ == '__main__'):
    start_server()