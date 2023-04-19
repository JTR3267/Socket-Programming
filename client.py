from tkinter import *
import socket

PORT = 7000
FORMAT = 'utf-8'
SERVER = "192.168.249.109" #將運行server得到的ip位址paste過來
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

current_page=0

def view1():
    msgtoserver = 'view ' + str((current_page-1)*5+1)
    client.send(msgtoserver.encode(FORMAT))
    recv=client.recv(1024).decode(FORMAT)
    if recv!=' ':
        read_context_label.config(text=recv)
        user_window.pack_forget()
        view_window.pack()

def view2():
    msgtoserver = 'view ' + str((current_page - 1) * 5 + 2)
    client.send(msgtoserver.encode(FORMAT))
    recv = client.recv(1024).decode(FORMAT)
    if recv != ' ':
        read_context_label.config(text=recv)
        user_window.pack_forget()
        view_window.pack()

def view3():
    msgtoserver = 'view ' + str((current_page - 1) * 5 + 3)
    client.send(msgtoserver.encode(FORMAT))
    recv = client.recv(1024).decode(FORMAT)
    if recv != ' ':
        read_context_label.config(text=recv)
        user_window.pack_forget()
        view_window.pack()

def view4():
    msgtoserver = 'view ' + str((current_page - 1) * 5 + 4)
    client.send(msgtoserver.encode(FORMAT))
    recv = client.recv(1024).decode(FORMAT)
    if recv != ' ':
        read_context_label.config(text=recv)
        user_window.pack_forget()
        view_window.pack()

def view5():
    msgtoserver = 'view ' + str((current_page - 1) * 5 + 5)
    client.send(msgtoserver.encode(FORMAT))
    recv = client.recv(1024).decode(FORMAT)
    if recv != ' ':
        read_context_label.config(text=recv)
        user_window.pack_forget()
        view_window.pack()

def send():
    receiver=receiver_entry.get()
    content=content_entry.get(1.0, 'end-1c')
    if receiver!='' and content!='':
        msgtoserver = 'send_message ' + receiver + ' ' + content
        client.send(msgtoserver.encode(FORMAT))
        recv = client.recv(1024).decode(FORMAT)
        if recv=='success':
            send_remind_label.config(text='已寄出')
            receiver_var.set('')
            content_entry.delete(1.0,'end')
        else:
            send_remind_label.config(text='找不到收信人')
            receiver_var.set('')
    else:
        send_remind_label.config(text='欄位不能為空')

def back_to_user():
    send_remind_label.config(text='')
    read_context_label.config(text='')
    receiver_var.set('')
    content_entry.delete(1.0,'end')
    send_window.pack_forget()
    view_window.pack_forget()
    refresh()
    user_window.pack()

def login():
    account=account_entry.get()
    password=password_entry.get()
    if account!='' and password!='':
        msgtoserver = 'login ' + account
        client.send(msgtoserver.encode(FORMAT))
        recv = client.recv(1024).decode(FORMAT)
        if recv=='Enter password':
            msgtoserver = password
            client.send(msgtoserver.encode(FORMAT))
            recv = client.recv(1024).decode(FORMAT)
            if recv=='success':
                account_var.set('')
                password_var.set('')
                login_remind_label.config(text='')
                next_page()
                login_window.pack_forget()
                user_window.pack()
            else:
                password_var.set('')
                login_remind_label.config(text=recv)
        else:
            login_remind_label.config(text=recv)
            account_var.set('')
            password_var.set('')
    else:
        login_remind_label.config(text='欄位不能留空')

def zero_handle():
    global current_page
    current_page=1
    message1_label.config(text='')
    message2_label.config(text='')
    message3_label.config(text='')
    message4_label.config(text='')
    message5_label.config(text='')

def front_page():
    global current_page
    if current_page>1:
        current_page=current_page-1
        msgtoserver ='sender '+str((current_page-1)*5+1)
        client.send(msgtoserver.encode(FORMAT))
        sender1_label.config(text=client.recv(1024).decode(FORMAT))
        msgtoserver = 'read_message '+str((current_page-1)*5+1)
        client.send(msgtoserver.encode(FORMAT))
        message1_label.config(text=client.recv(1024).decode(FORMAT))

        msgtoserver = 'sender ' + str((current_page - 1) * 5 + 2)
        client.send(msgtoserver.encode(FORMAT))
        sender2_label.config(text=client.recv(1024).decode(FORMAT))
        msgtoserver = 'read_message ' + str((current_page - 1) * 5 + 2)
        client.send(msgtoserver.encode(FORMAT))
        message2_label.config(text=client.recv(1024).decode(FORMAT))

        msgtoserver = 'sender ' + str((current_page - 1) * 5 + 3)
        client.send(msgtoserver.encode(FORMAT))
        sender3_label.config(text=client.recv(1024).decode(FORMAT))
        msgtoserver = 'read_message ' + str((current_page - 1) * 5 + 3)
        client.send(msgtoserver.encode(FORMAT))
        message3_label.config(text=client.recv(1024).decode(FORMAT))

        msgtoserver = 'sender ' + str((current_page - 1) * 5 + 4)
        client.send(msgtoserver.encode(FORMAT))
        sender4_label.config(text=client.recv(1024).decode(FORMAT))
        msgtoserver = 'read_message ' + str((current_page - 1) * 5 + 4)
        client.send(msgtoserver.encode(FORMAT))
        message4_label.config(text=client.recv(1024).decode(FORMAT))

        msgtoserver = 'sender ' + str((current_page - 1) * 5 + 5)
        client.send(msgtoserver.encode(FORMAT))
        sender5_label.config(text=client.recv(1024).decode(FORMAT))
        msgtoserver = 'read_message ' + str((current_page - 1) * 5 + 5)
        client.send(msgtoserver.encode(FORMAT))
        message5_label.config(text=client.recv(1024).decode(FORMAT))

def next_page():
    global current_page
    msgtoserver = 'show_message'
    client.send(msgtoserver.encode(FORMAT))
    message_amount = int(client.recv(1024).decode(FORMAT))
    if message_amount==0:
        zero_handle()
    elif current_page<((message_amount-1)//5+1):
        current_page=current_page+1
        msgtoserver = 'sender ' + str((current_page - 1) * 5 + 1)
        client.send(msgtoserver.encode(FORMAT))
        sender1_label.config(text=client.recv(1024).decode(FORMAT))
        msgtoserver = 'read_message ' + str((current_page - 1) * 5 + 1)
        client.send(msgtoserver.encode(FORMAT))
        message1_label.config(text=client.recv(1024).decode(FORMAT))

        msgtoserver = 'sender ' + str((current_page - 1) * 5 + 2)
        client.send(msgtoserver.encode(FORMAT))
        sender2_label.config(text=client.recv(1024).decode(FORMAT))
        msgtoserver = 'read_message ' + str((current_page - 1) * 5 + 2)
        client.send(msgtoserver.encode(FORMAT))
        message2_label.config(text=client.recv(1024).decode(FORMAT))

        msgtoserver = 'sender ' + str((current_page - 1) * 5 + 3)
        client.send(msgtoserver.encode(FORMAT))
        sender3_label.config(text=client.recv(1024).decode(FORMAT))
        msgtoserver = 'read_message ' + str((current_page - 1) * 5 + 3)
        client.send(msgtoserver.encode(FORMAT))
        message3_label.config(text=client.recv(1024).decode(FORMAT))

        msgtoserver = 'sender ' + str((current_page - 1) * 5 + 4)
        client.send(msgtoserver.encode(FORMAT))
        sender4_label.config(text=client.recv(1024).decode(FORMAT))
        msgtoserver = 'read_message ' + str((current_page - 1) * 5 + 4)
        client.send(msgtoserver.encode(FORMAT))
        message4_label.config(text=client.recv(1024).decode(FORMAT))

        msgtoserver = 'sender ' + str((current_page - 1) * 5 + 5)
        client.send(msgtoserver.encode(FORMAT))
        sender5_label.config(text=client.recv(1024).decode(FORMAT))
        msgtoserver = 'read_message ' + str((current_page - 1) * 5 + 5)
        client.send(msgtoserver.encode(FORMAT))
        message5_label.config(text=client.recv(1024).decode(FORMAT))

def refresh():
    global current_page
    msgtoserver = 'show_message'
    client.send(msgtoserver.encode(FORMAT))
    message_amount = int(client.recv(1024).decode(FORMAT))
    if message_amount==0:
        zero_handle()
    elif message_amount<current_page*5-4:
        current_page=current_page-1
    msgtoserver = 'sender ' + str((current_page - 1) * 5 + 1)
    client.send(msgtoserver.encode(FORMAT))
    sender1_label.config(text=client.recv(1024).decode(FORMAT))
    msgtoserver = 'read_message ' + str((current_page - 1) * 5 + 1)
    client.send(msgtoserver.encode(FORMAT))
    message1_label.config(text=client.recv(1024).decode(FORMAT))

    msgtoserver = 'sender ' + str((current_page - 1) * 5 + 2)
    client.send(msgtoserver.encode(FORMAT))
    sender2_label.config(text=client.recv(1024).decode(FORMAT))
    msgtoserver = 'read_message ' + str((current_page - 1) * 5 + 2)
    client.send(msgtoserver.encode(FORMAT))
    message2_label.config(text=client.recv(1024).decode(FORMAT))

    msgtoserver = 'sender ' + str((current_page - 1) * 5 + 3)
    client.send(msgtoserver.encode(FORMAT))
    sender3_label.config(text=client.recv(1024).decode(FORMAT))
    msgtoserver = 'read_message ' + str((current_page - 1) * 5 + 3)
    client.send(msgtoserver.encode(FORMAT))
    message3_label.config(text=client.recv(1024).decode(FORMAT))

    msgtoserver = 'sender ' + str((current_page - 1) * 5 + 4)
    client.send(msgtoserver.encode(FORMAT))
    sender4_label.config(text=client.recv(1024).decode(FORMAT))
    msgtoserver = 'read_message ' + str((current_page - 1) * 5 + 4)
    client.send(msgtoserver.encode(FORMAT))
    message4_label.config(text=client.recv(1024).decode(FORMAT))

    msgtoserver = 'sender ' + str((current_page - 1) * 5 + 5)
    client.send(msgtoserver.encode(FORMAT))
    sender5_label.config(text=client.recv(1024).decode(FORMAT))
    msgtoserver = 'read_message ' + str((current_page - 1) * 5 + 5)
    client.send(msgtoserver.encode(FORMAT))
    message5_label.config(text=client.recv(1024).decode(FORMAT))

def delete1():
    msgtoserver = 'delete_message ' + str((current_page - 1) * 5 + 1)
    client.send(msgtoserver.encode(FORMAT))
    refresh()

def delete2():
    msgtoserver = 'delete_message ' + str((current_page - 1) * 5 + 2)
    client.send(msgtoserver.encode(FORMAT))
    refresh()

def delete3():
    msgtoserver = 'delete_message ' + str((current_page - 1) * 5 + 3)
    client.send(msgtoserver.encode(FORMAT))
    refresh()

def delete4():
    msgtoserver = 'delete_message ' + str((current_page - 1) * 5 + 4)
    client.send(msgtoserver.encode(FORMAT))
    refresh()

def delete5():
    msgtoserver = 'delete_message ' + str((current_page - 1) * 5 + 5)
    client.send(msgtoserver.encode(FORMAT))
    refresh()

def go_to_send_window():
    user_window.pack_forget()
    send_window.pack()

def logout():
    global current_page
    msgtoserver = 'logout'
    client.send(msgtoserver.encode(FORMAT))
    user_window.pack_forget()
    login_window.pack()
    current_page=0

def go_to_register():
    login_remind_label.config(text='')
    account_var.set('')
    password_var.set('')
    login_window.pack_forget()
    register_window.pack()

def back():
    register_remind_label.config(text='')
    new_account_var.set('')
    new_password_var.set('')
    register_window.pack_forget()
    login_window.pack()

def register_new():
    account = new_account_entry.get()
    password = new_password_entry.get()
    if account!='' and password!='':
        if len(account)>10:
            register_remind_label.config(text='使用者名稱不得超過十個字元')
        else:
            msgtoserver = 'register '+account
            client.send(msgtoserver.encode(FORMAT))
            recv = client.recv(1024).decode(FORMAT)
            if recv=='Enter password':
                msgtoserver = password
                client.send(msgtoserver.encode(FORMAT))
                register_remind_label.config(text='註冊成功，2秒後自動返回登入頁面')
                new_account_var.set('')
                new_password_var.set('')
                win.after(2000,back)
            else:
                register_remind_label.config(text=recv)
                new_account_var.set('')
                new_password_var.set('')
    else:
        register_remind_label.config(text='欄位不能留空')

def socket_close():
    client.close()
    win.destroy()

win=Tk()
win.title('Simple Mail')
win.resizable(False,False)

login_window=Frame(win)
register_window=Frame(win)
user_window=Frame(win)
send_window=Frame(win)
view_window=Frame(win)

win.geometry("400x160")

#login_window
user_label=Label(login_window, text='帳號' )
user_label.grid(row=0 , column=0)
password_label=Label(login_window, text='密碼')
password_label.grid(row=1 , column=0)
account_var=StringVar()
password_var=StringVar()
account_entry=Entry(login_window, textvariable=account_var)
account_entry.grid(row=0 , column=1 )
password_entry=Entry(login_window, textvariable=password_var, show='*')
password_entry.grid(row=1 , column=1)
login_remind_label=Label(login_window, text='')
login_remind_label.grid(row=2, column=0, columnspan=2)
login_button=Button(login_window, text='登入', command=login, width=15, height=1)
login_button.grid(row=3 , column=0, columnspan=2)
register_button=Button(login_window, text='註冊新帳號', command=go_to_register, width=15, height=1)
register_button.grid(row=4 , column=0, columnspan=2)

#register_wondow
new_user_label=Label(register_window, text='新帳號' )
new_user_label.grid(row=0 , column=0)
new_password_label=Label(register_window, text='密碼')
new_password_label.grid(row=1 , column=0)
new_account_var=StringVar()
new_password_var=StringVar()
new_account_entry=Entry(register_window, textvariable=new_account_var)
new_account_entry.grid(row=0 , column=1 )
new_password_entry=Entry(register_window, textvariable=new_password_var, show='*')
new_password_entry.grid(row=1 , column=1)
register_remind_label=Label(register_window, text='')
register_remind_label.grid(row=2, column=0, columnspan=2)
new_register_button=Button(register_window, text='註冊', command=register_new, width=15, height=1)
new_register_button.grid(row=3 , column=0, columnspan=2)
back_button=Button(register_window, text='返回', command=back, width=15, height=1)
back_button.grid(row=4, column=0, columnspan=2)

#user_window
front_page_button=Button(user_window, text='上一頁', command=front_page, width=12, height=1)
front_page_button.grid(row=0, column=0)
next_page_button=Button(user_window, text='下一頁', command=next_page, width=12, height=1)
next_page_button.grid(row=0, column=1)
send_button=Button(user_window, text='寄信', command=go_to_send_window, width=12, height=1)
send_button.grid(row=0, column=2)
logout_button=Button(user_window, text='登出', command=logout, width=12, height=1)
logout_button.grid(row=0, column=3)
#column1
sender1_label=Label(user_window, text='', width=12, height=1)
sender1_label.grid(row=1, column=0)
message1_label=Label(user_window, text='', width=12, height=1)
message1_label.grid(row=1, column=1)
view1_button=Button(user_window, text='展開', command=view1, width=12, height=1)
view1_button.grid(row=1, column=2)
delete1_button=Button(user_window, text='刪除', command=delete1, width=12, height=1)
delete1_button.grid(row=1, column=3)
#column2
sender2_label=Label(user_window, text='', width=12, height=1)
sender2_label.grid(row=2, column=0)
message2_label=Label(user_window, text='', width=12, height=1)
message2_label.grid(row=2, column=1)
view2_button=Button(user_window, text='展開', command=view2, width=12, height=1)
view2_button.grid(row=2, column=2)
delete2_button=Button(user_window, text='刪除', command=delete2, width=12, height=1)
delete2_button.grid(row=2, column=3)
#column3
sender3_label=Label(user_window, text='', width=12, height=1)
sender3_label.grid(row=3, column=0)
message3_label=Label(user_window, text='', width=12, height=1)
message3_label.grid(row=3, column=1)
view3_button=Button(user_window, text='展開', command=view3, width=12, height=1)
view3_button.grid(row=3, column=2)
delete3_button=Button(user_window, text='刪除', command=delete3, width=12, height=1)
delete3_button.grid(row=3, column=3)
#column4
sender4_label=Label(user_window, text='', width=12, height=1)
sender4_label.grid(row=4, column=0)
message4_label=Label(user_window, text='', width=12, height=1)
message4_label.grid(row=4, column=1)
view4_button=Button(user_window, text='展開', command=view4, width=12, height=1)
view4_button.grid(row=4, column=2)
delete4_button=Button(user_window, text='刪除', command=delete4, width=12, height=1)
delete4_button.grid(row=4, column=3)
#column5
sender5_label=Label(user_window, text='', width=12, height=1)
sender5_label.grid(row=5, column=0)
message5_label=Label(user_window, text='', width=12, height=1)
message5_label.grid(row=5, column=1)
view5_button=Button(user_window, text='展開', command=view5, width=12, height=1)
view5_button.grid(row=5, column=2)
delete5_button=Button(user_window, text='刪除', command=delete5, width=12, height=1)
delete5_button.grid(row=5, column=3)

#send_window
send_back_button=Button(send_window, text='返回', command=back_to_user, width=10, height=1)
send_back_button.grid(row=4, column=0)
send_message_button=Button(send_window, text='寄出', command=send, width=10, height=1)
send_message_button.grid(row=4, column=2)
receiver_var=StringVar()
receiver_label=Label(send_window, text='收信人', width=10, height=1)
receiver_label.grid(row=0, column=0)
receiver_entry=Entry(send_window, textvariable=receiver_var, width=20)
receiver_entry.grid(row=0, column=1, columnspan=2)
content_label=Label(send_window, text='內文', width=10, height=3)
content_label.grid(row=1, column=0, rowspan=3)
content_entry=Text(send_window, width=20, height=3)
content_entry.grid(row=1, column=1, columnspan=2, rowspan=3)
send_remind_label=Label(send_window, text='', width=30)
send_remind_label.grid(row=5, column=0, columnspan=3)

#view_window
view_back_button=Button(view_window, text='返回', command=back_to_user, width=12, height=1)
view_back_button.grid(row=0, column=0, sticky='w')
read_context_label=Label(view_window, text='',width=48, height=5, wraplength = 330, anchor = 'nw', justify='left')
read_context_label.grid(row=1, column=0, columnspan=4, rowspan=5) #***

login_window.pack()
win.protocol("WM_DELETE_WINDOW", socket_close)
win.mainloop()