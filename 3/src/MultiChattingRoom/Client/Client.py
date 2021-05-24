'''
    Client.py
'''

from MultiChattingRoom.Setting import *


def main_window():
    # get configuration file
    # if there is not conf file, tips error
    file = open("ClientVersion.ini", "r", encoding="utf-8")
    version = file.read().split(":")[1]
    root = Tk()
    set_window_center(root, 340, 200)
    # set background colour
    root.configure(bg="white")
    # set title
    root.title("Chatting Room - version:" + version)
    # set create window
    pad, en_host, en_port = set_main_window(root)
    Label(root, text="Username:").grid(row=2, column=0, padx=pad, pady=pad)
    en_user = Entry(root)
    en_user.grid(row=2, column=1, padx=pad, pady=pad)
    en_user.focus_set()

    # component list
    widgets = {
        "en_host": en_host,
        "en_port": en_port,
        "en_user": en_user
    }
    # adding confirm button
    cfm_button = Button(root, text="Join the chatting room", command=lambda: verify_and_create(root, widgets))
    cfm_button.grid(rowspan=2, columnspan=2, padx=pad, pady=pad)
    # bind events
    root.bind("<Return>", lambda event: verify_and_create(root, widgets))
    # mainloop
    root.mainloop()


# verify the button event, checking the input is right or wrong
def verify_and_create(root, widgets):
    host, port, user = widgets["en_host"].get(), widgets["en_port"].get(), widgets["en_user"].get()
    # Port may be a string instead of number, you need to convert
    try:
        port = int(port)
    except error:
        # there is some characters in port, not just a number
        messagebox.showerror("Error", "Port must be number!")
        return
    # the input of host or port or user is null
    if not host or not port or not user:
        messagebox.showerror("Error", "Host or Port or Username can not be null!")
        return
    # start to create server socket
    addr = (host, port)
    try:
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(addr)
    except error as msg:
        messagebox.showerror("Error", "Can't create socket on " + str(addr) + "!")
        print(msg)
        return
    else:
        '''
            generate 2 queues
            main_queue is loop to get the sub process message in the main process
            sub_queue is loop to get the main process message in the sub process
            main process receive data
            sub process send data
        '''
        main_queue, sub_queue = Queue(), Queue()

        # send message of successful connection
        join_msg = str(user) + " has joined the chatting room.\n"
        client.send(join_msg.encode())

        # generate sub process
        sub_process = Process(target=deal_events, args=(client, sub_queue, main_queue))
        sub_process.daemon = True
        sub_process.start()

        # Create gui of chatting room
        create_chatroom(root, sub_queue, main_queue, user, join_msg)


# Create chatting room
def create_chatroom(r, sub_queue, main_queue, user, join_msg):
    # interface
    r.destroy()
    root = Tk()
    # center
    set_window_center(root, 500, 500)
    # minimize
    root.minsize(350, 350)
    # menu box
    menu = Menu(root)
    menu.add_command(label="Message")
    menu.add_command(label="Quit", command=root.destroy)
    root.config(menu=menu)
    # text box
    text = ScrolledText(root)
    text.pack(fill=BOTH)
    text.insert(END, join_msg)
    # input box
    inpu = Entry(root, bg='white', bd=5)
    inpu.pack(fill=BOTH, side=BOTTOM)
    inpu.focus_set()
    # send file button
    file_button = Button(root, text="send file", command=lambda: send_file(sub_queue, user))
    file_button.place(x=425, y=440)
    # bind events
    root.bind("<Return>", lambda event: send_msg(inpu, sub_queue, text, user))
    # title
    root.title("Chatting room - " + str(user))
    # background
    root.configure(bg="white")
    # set quit protocol
    root.protocol("WM_DELETE_WINDOW", lambda: quit_room(root, sub_queue, user))
    # main loop
    root.after(1000, recv_msg, root, main_queue, text)


def quit_room(root, sub_queue, user):
    data = user + " has quited the chatting room.\n"
    sub_queue.put(data)
    sleep(1)
    root.destroy()
    sys.exit(0)


# receive message
def recv_msg(root, main_queue, text):
    if not main_queue.empty():
        data = main_queue.get()
        # Server closed
        if data == 404:
            messagebox.showerror("Error", "Server has disconnected!")
            sys.exit(0)
        # receive file
        elif data == "/f".encode():
            recv_file(main_queue)
        else:
            text.insert(END, data)
    root.after(1000, recv_msg, root, main_queue, text)


def recv_file(main_queue):
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
    else:
        messagebox.showerror("Error", "File doesn't exist!")


# send message
def send_msg(inpu, sub_queue, text, user):
    time = ":".join(ctime().split()[3].split(":"))
    data = "[" + time + "]" + user + ":" + inpu.get() + "\n"
    text.insert(END, data)
    sub_queue.put(data)
    inpu.delete(0, END)


def send_file(sub_queue, user):
    file_path = filedialog.askopenfilename(title="Please choose a file")
    if os.path.exists(file_path):
        # pack file name and send to server
        fhead = struct.pack(b'128sq', bytes(os.path.basename(file_path), encoding='utf-8'),
                            os.stat(file_path).st_size)
        # put symbol, client name, file pack, file content
        sub_queue.put("/f")     # a symbol of file
        sub_queue.put(user.encode())
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
    else:
        messagebox.showerror("Error", "File doesn't exist!")


# deal receive and send events
def deal_events(client, sub_queue, main_queue):
    # set non-blocking I/O
    client.setblocking(0)
    byte_type = type(bytes(1))
    while True:
        if not sub_queue.empty():
            data = sub_queue.get()
            if data:
                if type(data) == byte_type:
                    client.send(data)
                else:
                    client.send(data.encode())
        try:
            data = client.recv(len_of_data)
            if type(data) != byte_type:
                data = data.decode()
        except BlockingIOError:
            continue
        except error:
            # server closed
            main_queue.put(404)
        else:
            main_queue.put(data)


if __name__ == "__main__":
    # detect configuration file
    path = "ClientVersion.ini"
    missing_conf(path, "Client")
    # detect version before running
    os.system("python Update.py")
    main_window()
