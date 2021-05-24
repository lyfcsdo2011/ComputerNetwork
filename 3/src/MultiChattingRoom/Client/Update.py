# encoding=utf-8
from MultiChattingRoom.Setting import *
from MultiChattingRoom.Client.killer import *


def detect_update():
    client_path = os.getcwd() + "\ClientVersion.ini"
    server_path = os.path.abspath(os.path.dirname(os.getcwd())) + "\Server\ServerVersion.ini"
    client_file = open(client_path, 'r', encoding="utf-8")
    server_file = open(server_path, "r", encoding="utf-8")
    server_info = server_file.read()
    client_version = float(client_file.read().split(":")[1])
    server_version = float(server_info.split(":")[1])
    flag = client_version < server_version
    client_file.close()
    # need update
    if flag:
        root = Tk()
        root.withdraw()
        cfm = messagebox.showinfo("Update detected.",
                                  "We detected a new version, do you want to update?",
                                  type="okcancel")
        if cfm == "ok":
            # kill old program
            kill_port(8080)
            update(client_path, server_info)
        else:
            return
    else:
        return


def update(cpath, ver):
    # delete client ini file
    os.remove(cpath)
    # save new
    file = open(cpath, "w", encoding="utf-8")
    file.write(ver)
    file.close()
    # progress
    progress_bar()


def progress_bar():
    root = Tk()
    set_window_center(root, 630, 150)
    root.title("Updating Program")
    # set progess bar
    Label(root, text="Download:", ).place(x=40, y=60)
    canvas = Canvas(root, width=465, height=22, bg="white")
    canvas.place(x=110, y=60)
    # display
    # fill the line
    fill_bar(root, canvas, 0.01, "green")


def fill_bar(root, canvas, time, color):
    file_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill=color)
    x = 500  # variable
    n = 465 / x
    for i in range(x):
        n = n + 465 / x
        canvas.coords(file_line, (0, 0, n, 60))
        root.update()
        sleep(time)
    sleep(0.5)
    root.destroy()
    root = Tk()
    root.withdraw()
    messagebox.showinfo("Success", "Update Success! Enjoy your self!", type="ok")


if __name__ == "__main__":
    detect_update()
