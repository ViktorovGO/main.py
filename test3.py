import os,sqlite3

def select_cmd(): #просмотр таблицы
    sql = 'SELECT * FROM {}'.format(tblname)
    with con:
        data = cur.execute(sql).fetchall()
   
    return (data)



dbname = input('Укажите имя файла SQLite: ') #ввод имени файла SQLite
if (os.path.isfile(dbname)!=True):
    print('Нет такого файла!')
else:
    tblname = input('Укажите имя таблицы: ') #ввод имени таблицы

    con = sqlite3.connect(dbname)
    cur = con.cursor()

    dan=select_cmd()

    nzap=len(dan)
    print('Таблица: ',tblname,' из БД ',dbname)
    for i in range(nzap):
        print(dan[i])


cur.close()
con.close()
