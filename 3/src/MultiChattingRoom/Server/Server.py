'''
    Server.py
    Using multithreading concurrent blokcing
'''

from MultiChattingRoom.Setting import *


def main_window():
    # get configuration file
    file = open("ServerVersion.ini")
    version = file.read().split(":")[1]
    # main window
    root = Tk()
    # set in the center
    set_window_center(root, 340)
    # set background colour
    root.configure(bg="white")
    # set title
    root.title("Chatting Room - version:" + version)
    # set size
    root.resizable(0, 0)
    # set create window
    pad, en_host, en_port = set_main_window(root)

    # component list
    widgets = {
        "en_host": en_host,
        "en_port": en_port
    }
    # adding confirm button
    cfm_button = Button(root, text="New Chatting room", command=lambda: verify_and_create(root, widgets))
    cfm_button.grid(rowspan=2, columnspan=2, padx=pad, pady=pad)
    # bind events
    root.bind("<Return>", lambda event: verify_and_create(root, widgets))
    # mainloop
    root.mainloop()


# verify the button event, checking the input is right or wrong
def verify_and_create(root, widgets):
    host, port = widgets["en_host"].get(), widgets["en_port"].get()
    # Port may be a string instead of number, you need to convert
    try:
        port = int(port)
    except error:
        # there is some characters in port, not just a number
        messagebox.showerror("Error", "Port must be number!")
        return
    # the input of host or port is null
    if not host or not port:
        messagebox.showerror("Error", "Host or Port can not be null!")
        return
    # start to create server socket
    addr = (host, port)
    try:
        server = socket(AF_INET, SOCK_STREAM)
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Port reuse
        server.bind(addr)
        server.listen(5)
    except error as msg:
        messagebox.showerror("Error", "Can't create socket on " + str(addr) + "!")
        print(msg)
        return
    # no error
    else:
        '''
            generate 2 queues
            main_queue is loop to get the sub process message in the main process
            sub_queue is loop to get the main process message in the sub process
            main process receive data
            sub process send data
        '''
        main_queue, sub_queue = Queue(), Queue()

        # generate sub process
        sub_process = Process(target=deal_events, args=(server, sub_queue, main_queue))
        sub_process.daemon = True
        sub_process.start()

        # Create gui of chatting room
        create_chatroom(root, sub_queue, main_queue)


# Create chatting room
def create_chatroom(r, sub_queue, main_queue):
    # interface
    r.destroy()
    root = Tk()
    # center
    set_window_center(root, 500, 500)
    # minimize
    root.minsize(350, 350)
    # menu box
    menu = Menu(root)
    menu.add_command(label="New")
    menu.add_command(label="Message")
    menu.add_command(label="Quit", command=root.destroy)
    root.config(menu=menu)
    # text box
    text = ScrolledText(root)
    text.pack(fill=BOTH)
    # send file button
    file_button = Button(root, text="send file", command=lambda: send_file(sub_queue, text))
    file_button.place(x=425, y=440)
    # input box
    inpu = Entry(root, bg='white', bd=5)
    inpu.pack(fill=BOTH, side=BOTTOM)
    inpu.focus_set()
    # bind enter events to send msg
    root.bind("<Return>", lambda event: send_msg(inpu, sub_queue, text))
    # title
    root.title("Chatting room - Administrator")
    # background
    root.configure(bg="white")
    # main loop
    root.after(1000, recv_msg, root, sub_queue, main_queue, text)
    note = "Administrator has created the chatting room.\n"
    text.insert(END, note)


# receive message
def recv_msg(root, sub_queue, main_queue, text):
    if not main_queue.empty():
        data = main_queue.get()
        if data == "/f".encode():
            recv_file(sub_queue, main_queue, text)
        else:
            text.insert(END, data)
    root.after(1000, recv_msg, root, sub_queue, main_queue, text)


# receive file
def recv_file(sub_queue, main_queue, text):
    user = main_queue.get()
    user = user.decode()
    recv_name = main_queue.get()  # Receive client pack file name, include lots of '\x00'
    if recv_name:
        filename, filesize = struct.unpack('128sq', recv_name)  # Unpack file
        filename = filename.decode()
        file = filename.strip('\x00')  # Remove '\x00', get real file name
        new_filename = os.path.join('./', "user_" + user + "_" + file)  # Store file at Server's current path
        # Start receiving less than 1024 bytes data from client,
        # if file size is too large, maybe receive many times
        # so we use 'while' loop to receive file.
        recv_size = 0
        fp = open(new_filename, 'wb')  # write
        while not recv_size == filesize:
            if filesize - recv_size > len_of_data:  # file size large than 1024 bytes
                data = main_queue.get()
                recv_size += len(data)
            else:
                data = main_queue.get()
                recv_size = filesize
            # print(f"Data is {data}")
            fp.write(data)  # write file data
        fp.close()
        client_msg = user + " has sent a file:" + file + ", please check in your file dir\n"
        text.insert(END, client_msg)
        sub_queue.put(client_msg)


# send message
def send_msg(inpu, sub_queue, text):
    time = ":".join(ctime().split()[3].split(":"))
    data = "[" + time + "]" + "Administrator:" + inpu.get() + "\n"
    sub_queue.put(data)
    text.insert(END, data)
    inpu.delete(0, END)


# send file
def send_file(sub_queue, text):
    usr = "Administrator"
    file_path = filedialog.askopenfilename(title="Please choose a file")
    file_name = file_path.split("/")[-1]
    if os.path.exists(file_path):
        # pack file name and send to server
        fhead = struct.pack(b'128sq', bytes(os.path.basename(file_path), encoding='utf-8'),
                            os.stat(file_path).st_size)
        # put symbol, client name, file pack, file content
        sub_queue.put("/f")     # a symbol of file
        sub_queue.put(usr.encode())
        sub_queue.put(fhead)
        # Start sending less than 1024 bytes data to server,
        # if file size is too large, maybe send many times
        # so we use 'while' loop to send file.
        fp = open(file_path, 'rb')  # read
        while True:
            data = fp.read(len_of_data)  # read 1024 bytes
            if not data:
                break
            sub_queue.put(data)
        admin_msg = "Administrator has sent a file:" + file_name + ", please check in your file dir\n"
        sub_queue.put(admin_msg)
        text.insert(END, admin_msg)
    else:
        messagebox.showerror("Error", "File doesn't exist!")


# deal receive and send events
def deal_events(server, sub_queue, main_queue):
    sock_list = [server]
    x_list = []
    y_list = []
    # data type
    byte_type = type(bytes(1))
    while True:
        # server send data
        if not sub_queue.empty():
            data = sub_queue.get()
            for sock in sock_list:
                if sock is not server:
                    if type(data) == byte_type:
                        sock.send(data)
                    else:
                        sock.send(data.encode())

        ss, xs, yx = select(sock_list, x_list, y_list, 1)
        for s in ss:
            # server accept connection
            if s == server:
                conn, addr = s.accept()
                sock_list.append(conn)
            else:
                try:
                    # server receive data
                    data = s.recv(len_of_data)
                    if type(data) != byte_type:    # not a bytes type, need encode
                        data = data.decode()
                except error:
                    sock_list.remove(s)
                # server resend to other client
                else:
                    main_queue.put(data)
                    for client in sock_list:
                        if client is not server and client is not s:
                            if type(data) == byte_type:
                                client.send(data)
                            else:
                                client.send(data.encode())


if __name__ == "__main__":
    # detect configuration file
    path = "ServerVersion.ini"
    missing_conf(path, "Server")
    main_window()


