import socket
import threading

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 7000
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

users={}

mapping={}

class Mail_box:
    def __init__(self, user_name):
        self.user_name = user_name
        self.mail_box = ['歡迎來到simple mail, 開始傳送email吧!']
        self.sender_box = ['Simple mail']
    def mail_box_len(self):
        return len(self.mail_box)
    def first_5_c(self, i):
        str=''
        count=0
        for c in self.mail_box[i]:
            if count<5:
                if c!='\n':
                    str=str+c
                    count=count+1
            else:
                break
        return str

def check_exist(name):
    for user in users.keys():
        if name == user:
            return True
    return False

def correct_message(list1):
    str=list1[2]
    if len(list1)>=4:
        for message in list1[3:]:
            str+=' '
            str+=message
    return str

def handle_client(conn, addr):
    loginuser = 'none'
    connect = True
    while connect:
        try:
            msg = conn.recv(1024).decode(FORMAT)
            split_msg=msg.split(' ')
            if split_msg[0]=='register':
                if check_exist(split_msg[1]):
                    sendtoclient='使用者名稱已被註冊'
                    conn.send(sendtoclient.encode(FORMAT))
                else:
                    sendtoclient = 'Enter password'
                    conn.send(sendtoclient.encode(FORMAT))
                    password = conn.recv(1024).decode(FORMAT)
                    users[split_msg[1]] = password
                    new_mail_box=Mail_box(split_msg[1])
                    mapping[split_msg[1]]=new_mail_box
            elif split_msg[0]=='login':
                if check_exist(split_msg[1]):
                    sendtoclient = 'Enter password'
                    conn.send(sendtoclient.encode(FORMAT))
                    password = conn.recv(1024).decode(FORMAT)
                    if password == users[split_msg[1]]:
                        loginuser=split_msg[1]
                        sendtoclient = 'success'
                        conn.send(sendtoclient.encode(FORMAT))
                    else:
                        sendtoclient = '密碼錯誤'
                        conn.send(sendtoclient.encode(FORMAT))
                else:
                    sendtoclient = '使用者名稱錯誤'
                    conn.send(sendtoclient.encode(FORMAT))
            elif split_msg[0]=='view':
                if int(split_msg[1]) <= mapping[loginuser].mail_box_len():
                    sendtoclient = mapping[loginuser].mail_box[mapping[loginuser].mail_box_len()-int(split_msg[1])]
                    conn.send(sendtoclient.encode(FORMAT))
                else:
                    sendtoclient = ' '
                    conn.send(sendtoclient.encode(FORMAT))
            elif split_msg[0]=='logout':
                loginuser='none'
            elif split_msg[0]=='show_message':
                sendtoclient = str(mapping[loginuser].mail_box_len())
                conn.send(sendtoclient.encode(FORMAT))
            elif split_msg[0] == 'read_message':
                if int(split_msg[1])<=mapping[loginuser].mail_box_len():
                    if len(mapping[loginuser].mail_box[mapping[loginuser].mail_box_len()-int(split_msg[1])])<=5:
                        sendtoclient=mapping[loginuser].mail_box[mapping[loginuser].mail_box_len()-int(split_msg[1])]
                        conn.send(sendtoclient.encode(FORMAT))
                    else:
                        sendtoclient = mapping[loginuser].first_5_c(mapping[loginuser].mail_box_len()-int(split_msg[1]))+'...'
                        conn.send(sendtoclient.encode(FORMAT))
                else:
                    sendtoclient = ' '
                    conn.send(sendtoclient.encode(FORMAT))
            elif split_msg[0] == 'send_message':
                if check_exist(split_msg[1]):
                    message=correct_message(split_msg)
                    mapping[split_msg[1]].mail_box.append(message)
                    mapping[split_msg[1]].sender_box.append(loginuser)
                    sendtoclient = 'success'
                    conn.send(sendtoclient.encode(FORMAT))
                else:
                    sendtoclient = 'Error user name'
                    conn.send(sendtoclient.encode(FORMAT))
            elif split_msg[0] == 'sender':
                if int(split_msg[1]) <= mapping[loginuser].mail_box_len():
                    sendtoclient = mapping[loginuser].sender_box[mapping[loginuser].mail_box_len()-int(split_msg[1])]
                    conn.send(sendtoclient.encode(FORMAT))
                else:
                    sendtoclient = ' '
                    conn.send(sendtoclient.encode(FORMAT))
            elif split_msg[0] == 'delete_message':
                if int(split_msg[1])<=mapping[loginuser].mail_box_len():
                    del mapping[loginuser].mail_box[mapping[loginuser].mail_box_len()-int(split_msg[1])]
                    del mapping[loginuser].sender_box[mapping[loginuser].mail_box_len()-int(split_msg[1])]
        except:
            connect=False

def start():
    conn, addr = server.accept()
    threading._start_new_thread(handle_client,(conn, addr))

print("[STARTING] Server is starting...")
print(f"[LISTENING] Server is listening on {SERVER}")
server.listen(10)
while True:
    start()