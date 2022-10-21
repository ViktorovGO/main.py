import os
import sqlite3
os.chdir("D:\\Учёба\\5 сем\\ПО\\НИР\\")
def DB(sql):  #Внесение изменений в БД
    if sql != '':
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

def ch_bd(con,cur):  #Запись таблицы в переменную
    sql= 'SELECT * FROM {}'.format(tbl_name)

    with con:
        BD= cur.execute(sql).fetchall()
    return BD

def out_bd(BD):  #Вывод БД в виде таблицы
    leng=len(BD)
    print('Таблица: ', tbl_name, ' из БД ', db_name)
    for i in range(leng):
        print(BD[i])

def save_bd_txt(BD,fil_name,fil): # Запись БД в файл с заданным именем
    fil.write('Таблица с именем: ' + tbl_name + ' из базы данных с именем:  ' + db_name + '\n')
    for i in range(len(BD)):
        fil.write(str(BD[i]) + "\n")

def del_str_bd(usl):   #Удаление строки
    sql = 'DELETE FROM {}'.format(tbl_name)
    if usl != '':
        sql += ' WHERE {}'.format(usl)
    DB(sql)

def change_bd(usl):    #Замена значений
    j = int(input("Введите количество полей для изменения: "))
    str = ""
    for i in range(j):
        cng = input('Введите имя поля: ')
        cng_znach = input('Введите значение, на которое заменить поле: ')
        str += cng + "=" + cng_znach + ","
    str = str[:-1]   # Удаляем последнюю запятую
    sql = 'UPDATE {} SET {} WHERE {}'.format(tbl_name,str, usl)
    DB(sql)

def out_usl_bd(usl_1,n=1):  # Отображение подмножества строк, удовлетворяющих заданному условию

    if(n>1):
        names=""
        for i in range(n):
            names+=input("Введите имя столбца ")+" "
        names=names[:-1] #Удаляем последний пробел
        names=",".join(names.split())
        sql = 'SELECT {} FROM {} WHERE {}'.format(names,tbl_name, usl_1)

    else:
        sql = 'SELECT * FROM {} WHERE {}'.format(tbl_name,usl_1)
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    with con:
        BD= cur.execute(sql).fetchall()
    cur.close()
    con.close()
    out_bd(BD)

def insert_bd(bd_headers):   # добавление строки в БД
    n = int(input("Введите количество строк для записи: "))
    for j in range(n):
        str=()
        for i in bd_headers:
            if i=="dis_date" or i=="entry_date":
                print("Дата вводится в формате ДД.ММ.ГГ")
            x = input("Введите значение для {}: ".format(i))
            if x.isnumeric():
                str += int(x),
            else:
                str += x,
        print(type(str))
        sql='INSERT INTO {} {} VALUES {}'.format(tbl_name,bd_headers,str)
        DB(sql)

def main():
    global db_name
    global tbl_name
    db_name= input('Укажите имя файла SQLite: ') #ввод имени файла SQLite
    flag=True

    if (os.path.isfile(db_name)!=True):
        print('Нет такого файла!')
        flag=False

    if flag==True:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        tbl_name = cur.execute("SELECT name FROM sqlite_master WHERE TYPE = 'table'").fetchall()[0][0]
        BD = ch_bd(con,cur)
        cur.close()
        con.close()

    while(flag):
        what=int(input("""
        Выберите действие(Введите цифру):
        1 - Отображение текущего содержимого БД на экране в виде таблицы
        2 - Сохранение таблицы в текстовый файл с задаваемым именем
        3 - Выбор операции: удаление из БД, замена значений на заданное
        4 - Выбор пользователем имени одного из полей БД и задание условия по значениям этого поля (логическое выражение). Отображение подмножества строк, удовлетворяющих заданному условию.
        5 - Добавление строки в БД
        6 - Завершение работы с программой
    
        """))
        if what==1:
            con = sqlite3.connect(db_name)
            cur = con.cursor()
            BD = ch_bd(con,cur)
            cur.close()
            con.close()
            out_bd(BD)

        if what==2:
            fil_name = input("Введите имя файла: ")
            fil = open(fil_name, 'w')
            save_bd_txt(BD,fil_name,fil)
            fil.close()
            print("Информация из таблицы ", db_name, "сохранена в файл", fil_name)

        if what==3:
            operation=int(input("""
            Выберете операцию(Введите цифру):
            1 - Удаление строки
            2 - Замена значений на заданное
            """))
            usl=input("Введите условие ")
            if operation==1:
                del_str_bd(usl)
            if operation==2:
                change_bd(usl)

        if what==4:
            usl_1=input("Введите условие(Например ... > ...) ")
            do=int(input("""
            1 - Вывести все поля таблицы
            2 - Задать необходимые поля
            """))
            if(do==1):
                out_usl_bd(usl_1)
            if(do==2):
                n = int(input("Введите количество полей "))
                out_usl_bd(usl_1,n)

        if what==5:
            con = sqlite3.connect(db_name)
            cur = con.cursor()
            sql = 'SELECT name FROM PRAGMA_TABLE_INFO("{}")'.format(tbl_name)
            x=cur.execute(sql).fetchall()
            bd_headers =tuple(bd_headers[0] for bd_headers in x)
            cur.close()
            con.close()
            insert_bd(bd_headers)

        if what==6:
            break

main()
