'''
    Server.py
    Using multithreading concurrent blokcing
'''

from socket import *
import os
import threading
import time
import sys
import struct       # pack file


def socket_server():
    try:
        server = socket(AF_INET, SOCK_STREAM)
        # Prevent port occupancy
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # Bind IP and port
        server.bind(("192.168.43.232", 8080))   # 127.0.0.1
        # Listen
        server.listen(5)
    except error as msg:
        print(msg)
        sys.exit(1)

    print("Waiting for connection...")

    while True:
        # Accept connect
        conn, addr = server.accept()    # addr = (ip, port)
        print("Accept connection from Client" + str(addr))
        conn.send('Connect Success!'.encode())
        # Multithreading
        thred = threading.Thread(target=deal_message, args=(conn, addr))
        thred.start()


def deal_message(conn, addr):
    while True:
        try:
            data_type = conn.recv(1024).decode()
        except error as msg:
            print("Client" + str(addr) + "has been closed")
            break
        print("Data type comes from Client" + str(addr) + ":" + str(data_type))
        # Receive messages
        # First receive message type from client, 0 is exit, 1 is message, 2 is file
        if data_type == '0':
            print("Client " + str(addr) + " has been closed")
            conn.send('Connection closed!'.encode())
            print()
            print("Waiting for connection...")
            break
        elif data_type == '1':
            data = conn.recv(1024).decode()
            print("Messages come from Client" + str(addr) + ":" + str(data))
            time.sleep(1)
            if data == 'exit' or not data:
                print("Client" + str(addr) + " has been closed")
                conn.send('Connection closed!'.encode())
                print()
                print("Waiting for connection...")
                break
            conn.send('Send Success!'.encode())
        # Receive pictures
        elif data_type == '2':
            flag = conn.recv(1024).decode()
            if flag == "Y":
                file_size = struct.calcsize('128sq')                      # Pack file at '128sq' form
                recv_name = conn.recv(file_size)                          # Receive client pack file name, include lots of '\x00'
                if recv_name:
                    filename, filesize = struct.unpack('128sq', recv_name)     # Unpack file
                    file = filename.decode().strip('\x00')                # Remove '\x00', get real file name
                    print("Receive a file from client: " + str(file) + ", size is " + str(filesize) + " bytes")
                    new_filename = os.path.join('./', 'new_' + file)      # Store file at Server's current path

                    # Start receiving less than 1024 bytes data from client,
                    # if file size is too large, maybe receive many times
                    # so we use 'while' loop to receive file.
                    recv_size = 0
                    fp = open(new_filename, 'wb')               # write
                    while not recv_size == filesize:
                        if filesize - recv_size > 1024:         # file size large than 1024 bytes
                            data = conn.recv(1024)
                            recv_size += len(data)
                        else:
                            data = conn.recv(1024)
                            recv_size = filesize
                        # print(f"Data is {data}")
                        fp.write(data)                          # write file data
                    fp.close()
                    print("File " + str(file) + " has been stored at current path as " + str(new_filename))
                    conn.send('Send Success!'.encode())
            else:
                print("File does not exists!")
        print()
    conn.close()


if __name__ == '__main__':
    socket_server()
