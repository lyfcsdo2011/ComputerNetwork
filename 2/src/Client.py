from socket import *
import os
import sys
import struct


def socket_client():
    try:
        client = socket(AF_INET, SOCK_STREAM)       # create
        client.connect(("192.168.43.232", 8080))         # connect
    except error as msg:
        print(msg)
        sys.exit(1)

    print(client.recv(1024).decode())
    while True:
        msg_type = input("Please input data type you want to send(close:0, msg:1 ,file:2):")
        client.send(msg_type.encode())
        # input 0:close, input 1:send message, input 2:send file
        if msg_type == '0':
            print(client.recv(1024).decode())
            break
        if msg_type == '1':
            msg = input("Please input message you want to send:")
            client.send(msg.encode())
            print(client.recv(1024).decode())
            if msg == 'exit':
                break
        elif msg_type == '2':
            filepath = input("Please input the file:")      # Current path
            if os.path.exists(filepath):
                client.send("Y".encode())
                # pack file name and send to server
                fhead = struct.pack(b'128sq', bytes(os.path.basename(filepath), encoding='utf-8'),
                                    os.stat(filepath).st_size)
                client.send(fhead)
                # Start sending less than 1024 bytes data to server,
                # if file size is too large, maybe send many times
                # so we use 'while' loop to send file.
                fp = open(filepath, 'rb')                       # read
                while True:
                    data = fp.read(1024)                        # read 1024 bytes
                    if not data:
                        print(str(filepath) + " has been sent over")
                        break
                    client.send(data)
                print(client.recv(1024).decode())
                print()
            else:
                client.send("N".encode())
                print("File does not exists!")
    client.close()


if __name__ == '__main__':
    socket_client()
