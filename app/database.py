from pymysql import Connection
import serial


#串口接收数据
def get_data() -> str:

    data = "0"
    ser = serial.Serial('COM5', 19200, timeout=200)
    while (True):
        data = ser.read_all()
        if(data != b''):
            data = str(data,'UTF-8')
            break
        #print("loading")
    ser.close()

    return data


#将快递包裹信息存入数据库
def save_data(data: str) -> bool:

    #链接本地数据库
    conn = Connection(
        host = "localhost",
        port = 3306,
        user = "root",
        password = "1919810"
    )

    #获取包裹信息
    number = data
    package_type = data[0]
    goods_type = data[1]
    sender_add = data[11:13]
    flag = 1
    wrong = "单号："+ data +"保存成功"

    #将代码转换为文字信息
    while(True):
        if(len(data) != 13):
            flag = 0
            wrong = "数据错误，请重新获取单号"
            
            break
    
        if(package_type == "E"):
            package_type = "EMS特快专递"
        elif(package_type == "R"):
            package_type = "国际邮政小包"
        elif(package_type == "C"):
            package_type = "国际邮政大包"
        else:
            wrong = "包裹单号格式错误，请核实信息是否正确"
            flag = 0
            break

        if(goods_type == "F"):
            goods_type = "食品"
        elif(goods_type == "C"):
            goods_type = "衣物"
        elif(goods_type == "V"):
            goods_type = "保价物品"
        else:
            wrong = "包裹单号格式错误，请核实信息是否正确"
            flag = 0
            break

        if(sender_add == "CN"):
            sender_add = "中国"
        elif(sender_add == "US"):
            sender_add = "美国"
        elif(sender_add == "JP"):
            sender_add = "日本"
        else:
            wrong = "包裹单号格式错误，请核实信息是否正确"
            flag = 0
        break

    #向数据库插入包裹信息
    try:
        if(flag):
            cursor = conn.cursor()
            conn.select_db('expressage')
            sql = f"INSERT INTO package VALUES ('{number}', '{package_type}', '{goods_type}', '{sender_add}')"
            cursor.execute(sql)
            cursor.connection.commit()   #若要保存执行结果，必须确认光标内容

        conn.close()
    except Exception as e:
        wrong = e
        conn.close()

    return wrong


#通过单号调取包裹信息
def number_select_data (number: str) -> str:

    #链接本地数据库
    conn = Connection(
        host = "localhost",
        port = 3306,
        user = "root",
        password = "1919810"
    )

    #从数据库查找数据
    cursor = conn.cursor()
    conn.select_db('expressage')
    sql1 = f"SELECT * FROM package WHERE number = '{number}'"
    cursor.execute(sql1)
    package = cursor.fetchall()
    conn.close()

    return package


#通过包裹类型调取包裹信息
def package_type_select_data(package_type: str) -> str:

    #链接本地数据库
    conn = Connection(
        host = "localhost",
        port = 3306,
        user = "root",
        password = "1919810"
    )

    #从数据库查找数据
    cursor = conn.cursor()
    conn.select_db('expressage')
    sql1 = f"SELECT * FROM package WHERE package_type = '{package_type}'"
    cursor.execute(sql1)
    package = cursor.fetchall()
    conn.close()

    return package


#通过物品类型调取包裹信息
def goods_type_select_data(goods_type: str) -> str:

    #链接本地数据库
    conn = Connection(
        host = "localhost",
        port = 3306,
        user = "root",
        password = "1919810"
    )

    #从数据库查找数据
    cursor = conn.cursor()
    conn.select_db('expressage')
    sql1 = f"SELECT * FROM package WHERE goods_type = '{goods_type}'"
    cursor.execute(sql1)
    package = cursor.fetchall()
    conn.close()

    return package


#通过发出地调取包裹信息
def sender_add_select_data(sender_add: str) -> str:

    #链接本地数据库
    conn = Connection(
        host = "localhost",
        port = 3306,
        user = "root",
        password = "1919810"
    )

    #从数据库查找数据
    cursor = conn.cursor()
    conn.select_db('expressage')
    sql1 = f"SELECT * FROM package WHERE sender_add = '{sender_add}'"
    cursor.execute(sql1)
    package = cursor.fetchall()
    conn.close()

    return package

