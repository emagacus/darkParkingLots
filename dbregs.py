import pymysql





# Ejecutar comandos
#cursor.execute(registro1)
#cursor.execute(registro2)
#cursor.execute(registro3)

# Finalizar transacción y cerrar
#conexion.commit()


def getStatusData():
    parking_id = 1
    # Conectar con base de datos
    conexion = pymysql.connect(host="localhost", 
                            user="root", 
                            passwd="root", 
                            database="q_test")
    #cursor = conexion.cursor()
    # Definir comandos para insertar registros
    #registro1 = "insert into registros(plate,frame_path,frame_coordinates,creation_date,direction,parking_id)values ('JKW5528','img.jpg','2019-05-19T16:08:51.809449','in',1);"
    cur = conexion.cursor()
    n = cur.execute('select * from status_parking where id = 1')
    c = cur.fetchall()

    print(c)
    #parking id
    for i in c:
        if i[2] is parking_id:
            conexion.close()
            return i
