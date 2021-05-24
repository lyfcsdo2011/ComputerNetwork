import os
import pandas as pd
'''
    based on windows cmd
'''

"""
  TCP    127.0.0.1:8080    127.0.0.1:23098    ESTABLISHED     11064
  TCP    127.0.0.1:8080    0.0.0.0            LISTENING       11064
"""


def kill_port(port):
    find_port = 'netstat -aon | findstr %s' % port
    result = os.popen(find_port)
    info = result.read().split('\n')
    data = []
    for line in info:
        if not line:
            continue
        temp = [str for str in line.split(" ") if str]
        data.append(temp)
        parser_cmd(data)


def parser_cmd(data):
    columns = ["type", "secret", "open", "status", "pid"]
    df = pd.DataFrame(data=data, columns=list(columns))
    for index in range(len(data)):
        pid = df.loc[index, 'pid']
        kill_pid(pid)


def kill_pid(pid):
    find_kill = 'taskkill -f -pid %s' % pid
    result = os.popen(find_kill)

