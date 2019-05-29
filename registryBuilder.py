#Registry builder

import datetime
import os
import cv2
import pymysql.cursors
import traceback
import requests
parkingId = 1

def initConfig():
    timestamp = datetime.datetime.now().isoformat()
    os.mkdir("log/"+str(timestamp),0o777)
    #os.mkdir("log/"+str(timestamp) + "/plates",0o777)
    return timestamp

#registro1 = "insert into registros(plate,frame_path,frame_coordinates,creation_date,direction,parking_id)values ('JKW5528','img.jpg','2019-05-19T16:08:51.809449','in',1);"

def registryQueryBuilder(plate,frame_path,date,direction,parking_id):
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='q_test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO registros(plate,frame_path,creation_date,direction,parking_id) VALUES (%s, %s,%s, %s,%s)"
            cursor.execute(sql, (plate,frame_path,date,direction,parking_id))
        
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    except Exception as e:
        tb = traceback.format_exc()
        print("error in insert",tb)
    finally:
        connection.close()

def getDirection(resultsArray,plates):
    #print("This is probably a car", resultsArray[0][1])
    y1Movement = resultsArray[0][2]
    y2Movement = resultsArray[0][4]
    directionY1 = 0
    directionY2 = 0
    best = 0
    direction = ""
    bestPlate = ""
    for plate in plates:
        #print("top plate found: ",plate[0]['plate'])
        if best <= float(plate[0]['confidence']):
            best = float(plate[0]['confidence'])
            bestPlate = plate[0]['plate']

    #print("best match",bestPlate)
    #print("with ",best)
    for result in resultsArray:
        #cv2.imwrite(str(datetime.datetime.now().isoformat())+".jpg",result[0])
        directionY1 = result[2]
        directionY2 = result[4]
    if directionY2 >= y2Movement:
        print("Auto en direccion sur")
        direction = "in"
        #return "north"
    elif directionY2 <= y2Movement:   
        print("Auto en direccion norte")
        direction = "out"
        #return "south"
    timestamp = datetime.datetime.now().isoformat()
    path = "plates/"+str(timestamp)+".jpg"
    cv2.imwrite(path,resultsArray[0][0])
    registryQueryBuilder(str(bestPlate),path,str(timestamp),direction,str(parkingId))
    data = getStatusData(parkingId)
    oc = data[1]
    fr = data[3]
    updateStatusAPI(fr,oc,parkingId)

    """    
    print("punto y1 inicial",y1Movement)
    print("punto y2 inicial",y2Movement)
    print("punto y1 final",directionY1)
    print("punto y2 final",directionY2)
    """
        
        
    
    

def createLogEntry(path,img,data):
    fileName = datetime.datetime.now().isoformat()
    cv2.imwrite("log/"+path+"/"+str(fileName)+".jpg",img)



def getStatusData(parkingId):
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
        if i[2] is parkingId:
            conexion.close()
            return i


def updateStatusAPI(freespaces , occupation, parking_id):
    
    try:
        url = "http://3.14.88.183:8001/status/1/"

        payload = "{\n    \"freespaces\":" + str(freespaces) + ",\n    \"occupied\": "+ str(occupation) +  ",\n    \"parking\": "+ str(parking_id) + "\n}"
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic ZW1hZ2FjYTpUZXN0aW5nLjEyMw==",
            'cache-control': "no-cache",
            'Postman-Token': "9ba70891-c98f-4109-a2c1-93a1312ce6c2"
            }

        response = requests.request("PUT", url, data=payload, headers=headers)

    except Exception as e:
        tb = traceback.format_exc()
        print("error in iput request ",tb)
        print("unable to put request")