import tkinter as tk
from database import * #get_data, save_data, number_select_data, package_type_select_data, goods_type_select_data, sender_add_select_data
import threading
from queue import Queue

data = Queue()
data.put("当前未收到单号")

#data = "当前未收到单号"

#获取数据
def get_text():
    while True:
        data.put(get_data())
        #log_text.insert(tk.END, data+ "\n")
        text = data.get()
        data_label.config(text=text)
        data.put(text)

#保存数据
def save_text():
    if(data.empty()):
        log_text.insert(tk.END, "当前存储单号为空，请重新扫描\n")
        data_label.config(text="当前未收到单号")
    else:
        save_info = save_data(data.get())
        log_text.insert(tk.END, save_info)
        log_text.insert(tk.END, "\n")

#单号查询
def select_text():
    input_text = input_var.get()
    log_text.insert(tk.END, "输入：" + input_text + "\n")
    if (number_select_data(input_text) == ()):
        log_text.insert(tk.END, "检索为空！\n")
    else:
        log_text.insert(tk.END, number_select_data(input_text))
        log_text.insert(tk.END, "\n")

#筛选信息
def screen_text():
    value = spinbox.get()
    log_text.insert(tk.END, "筛选"+ value +":\n")
    log_text.insert(tk.END, package_type_select_data(value) + goods_type_select_data(value) + sender_add_select_data(value))
    log_text.insert(tk.END, "\n")


#APP界面
if __name__ == "__main__":

    window = tk.Tk()
    window.title("快递数据管理系统")


    log_label = tk.Label(window, text="调试信息窗口：", width=32, height=1, anchor='w')
    log_label.grid(row=0, column=1, padx=(1, 12), pady=(4, 1))

    log_text = tk.Text(window, width=32, height=20)
    log_text.grid(row=1, column=1, rowspan=8, padx=(1, 12), pady=(1, 12))


    save_label = tk.Label(window, text="当前接收单号：", width=32, height=1, anchor="w")
    save_label.grid(row=0, column=0, padx=(12, 1), pady=(4, 1))

    data_label = tk.Label(window, text=data.get(), width=32, height=1)
    data_label.grid(row=1, column=0, padx=(12, 1), pady=(1, 4))

    save_button = tk.Button(window, text="保存当前单号", command=save_text, relief="raised", overrelief="ridge", width=20, height=1)
    save_button.grid(row=2, column=0, padx=(6, 1), pady=(1, 12))


    input_label = tk.Label(window, text="输入待查单号：", width=32, height=1, anchor="w")
    input_label.grid(row=3, column=0, padx=(12, 1), pady=(12, 1))

    input_var = tk.StringVar()
    input_entry = tk.Entry(window, textvariable=input_var)
    input_entry.grid(row=4, column=0, padx=(12, 1), pady=1)

    retrieve_button = tk.Button(window, text="查询输入单号", command=select_text, relief="raised", overrelief="ridge",width=20, height=1)
    retrieve_button.grid(row=5, column=0, padx=(12, 1), pady=(1, 12))


    screen_label = tk.Label(window, text="筛选特定信息：", width=32, height=1, anchor="w")
    screen_label.grid(row=6, column=0, padx=(12, 1), pady=(12, 1))

    spinbox = tk.Spinbox(window, values=("EMS特快专递", "国际邮政小包", "国际邮政大包", "食品", "衣物", "保价物品", "中国", "美国", "日本"))
    spinbox.grid(row=7, column=0, padx=(12, 1), pady=(1, 1))
    
    screen_button = tk.Button(window, text="筛选上述信息", command=screen_text, relief="raised", overrelief="ridge", width=20, height=1)
    screen_button.grid(row=8, column=0, padx=(12, 1), pady=(1, 12))

    #数据获取线程
    thread = threading.Thread(target=get_text)
    thread.start()

    window.mainloop()
