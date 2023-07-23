#Clase de acceso a la base de datos cronosDB
import mysql.connector
from mysql.connector import errors

from datetime import datetime

from sortedcontainers import SortedList
#pip install sortedcontainers
import bisect

class Datos():
    def __init__(self, user:str, password:str, host=str, database=str):
        self._config = {'user':user,'password':password,'host':host,'database':database}
        self.date = datetime.today()
    
    @property
    def date(self):
        return self._date
    @date.setter
    def date(self, date:datetime):
        self._date = date
        self._events_for_month()
        self._classify_events_by_day()

    def connectBD(self):
        try:
            self._conection = mysql.connector.connect(**self._config)
        except errors.InterfaceError as error:
            print("Error en la conexion con la base de datos.")
            if error.errno == 2003:
                print("No se puede conectar al servidor de MySQL. {}".format(error))
            elif error.errno == 2002:
                print("No se puedo resolver el nombre de host o la direccion IP del servidor MySQL. {}".format(error))
            elif error.errno == 2013:
                print("Se perdio la conexión al servidor durante una consulta. {}".format(error))
            elif error.errno == 2014:
                print("Se agotó el tamaño del búfer del cliente duranta la lectura de resultados del servidor. {}".format(error))
            elif error.errno == 2055:
                print("No se pudo establecer una conexion al servidor MySQL debido a un numero maxiomo de conexiones alcanzado. {}".format(error))
            else:
                print("Código de error no registrado. ERROR: {}".format(error))
        except errors.DatabaseError as error:
            print("Se encontro un error con la base de datos.")
            if error.errno == 1044:
                print("Acceso denegado para el usuario '{}'@'{}' en la base de datos -> {}".format(**(self._config[0],
                                                                                                      self._config[2],
                                                                                                      self._config[3])))
            elif error.errno == 1045:
                print("Error de acceso: No se pudo conectar a la base de datos. ")
                print("Verifica las credenciales del usuario y/o contraseña.")
            else:
                print(error)
    
    def _events_for_month(self):
        self.connectBD()
        try:
            cursor = self._conection.cursor()
            #Generamos la consulta para obtener todos los eventos de un mes en espefico.
            query = """SELECT * FROM eventos WHERE YEAR(fecha_y_hora_e) = %s AND MONTH(fecha_y_hora_e) = %s ORDER BY fecha_y_hora_e DESC"""
            cursor.execute(query, (self.date.year,self.date.month))
            self._month_events = cursor.fetchall()
        except errors.DatabaseError as error:
            if error.errno == 1046:
                print("Error en la base de datos, la tabla 'eventos' no existe")
            else:
                print(error)
        cursor.close()
        self._conection.close()
    
    def tags_cross_idEvent(self, idEvent):
        self.connectBD()
        cursor = self._conection.cursor()

        query = """SELECT tag.nombre FROM eventos e
        INNER JOIN evento_etiqueta evtag ON e.idEvento = evtag.idEvento
        INNER JOIN etiquetas tag ON evtag.idEtiqueta = tag.idEtiqueta
        WHERE e.idEvento = %s"""

        cursor.execute(query, (idEvent,))

        response = cursor.fetchall()
        if len(response) != 0:
            tags = response[0]
        else:
            tags = ()
        
        cursor.close()
        self._conection.close()
        
        return tags

    def _addday(self, event):
        day = event[3].day
        if day in self.eventsbyday:
            self.eventsbyday[day].add(list(event))
        else:
            self.eventsbyday[day] = SortedList([list(event)], key = lambda x: x[4])

    def _classify_events_by_day(self):
        self.eventsbyday = {}
        for event in self._month_events:
            self._addday(event)
    
    def new_event(self, title:str, duration:int, datetimeE:datetime, datetimeR:datetime, detail:str, relevance:int, tags:tuple=None):
        #Conexion con la base de datos
        self.connectBD()
        #Crea un nuevo evento en la tabla eventos
        query = """INSERT INTO eventos (titulo, duracion, fecha_y_hora_e, fecha_y_hora_r, detalle, import)
        VALUES (%s,%s,%s,%s,%s,%s)"""
        cursor = self._conection.cursor()
        cursor.execute(query,(title,str(duration),datetimeE.strftime('%Y-%m-%d %H:%M:%S'),datetimeR.strftime('%Y-%m-%d %H:%M:%S'), detail, str(relevance)))
        #obtenemos el id del ultimo evento ingresado
        idEvent = cursor.lastrowid
        print(idEvent)
        #Crea las etiquetas correspondientes al evento, si las hay
        self._associate_tags(cursor, idEvent, tags)
        event = [idEvent, title, duration, datetimeE, datetimeR, detail, relevance]
        if self.date.month == datetimeE.month and self.date.year == datetimeE.year:
            self._addday(event)
        self._conection.commit()
        cursor.close()
        self._conection.close()
    
    def _associate_tags(self, cursor, idEvent:int, tags:tuple):
        if tags != None:
            tags_id_list = []
            for tag in tags:
                print(tag)
                query = """SELECT idEtiqueta FROM etiquetas
                WHERE etiquetas.nombre = %s"""
                cursor.execute(query, (tag,))
                response = cursor.fetchall()
                if len(response) != 0:
                    tags_id_list.append(response[0][0])
                else:
                    query = """INSERT INTO etiquetas (nombre) VALUES (%s)"""
                    cursor.execute(query, (tag,))
                    tags_id_list.append(cursor.lastrowid)
            #Crea las relaciones entre la tabla eventos y etiquetas
            for id_tag in tags_id_list:
                query = """INSERT INTO evento_etiqueta (idEvento, idEtiqueta)
                VALUES (%s, %s)"""
                cursor.execute(query,(str(idEvent),str(id_tag)))

    @staticmethod
    def _bisect(lis, wanted):
        start = 0
        end = len(lis) - 1
        while start<=end:
            mid = (start + end) // 2
            if lis[mid] != wanted:
                if lis[mid] > wanted:
                    end = mid - 1
                else:
                    start = mid + 1
            else:
                return mid
        return -1

    def modifyevent(self, id:int, title:str, duration:int, datetimeE:datetime, datetimeR:datetime, detail:str, relevance:int, tags:tuple=None):
        self.connectBD()
        query = """UPDATE eventos SET
        titulo = %s,
        duracion = %s,
        fecha_y_hora_e = %s,
        fecha_y_hora_r = %s,
        detalle = %s,
        import = %s
        WHERE idEvento = %s"""
        cursor = self._conection.cursor()
        cursor.execute(query, (title,duration,datetimeE,datetimeR,detail,relevance,id))
        if tags!=None:
            query = """SELECT tag.idEtiqueta, tag.nombre
            FROM eventos ev
            INNER JOIN evento_etiqueta ev_tag ON ev.idEvento = ev_tag.idEvento
            INNER JOIN etiquetas tag ON ev_tag.idEtiqueta = tag.idEtiqueta
            WHERE ev.idEvento = %s
            ORDER BY tag.nombre"""
            cursor.execute(query, (id,))
            response = cursor.fetchall()
            print(f"response={response}")
            oldids = [x[0] for x in response]
            print(f"oldids={oldids}")
            oldtags = [x[1] for x in response]
            print(f"oldtags={oldtags}")
            newtags= []
            disposableids = []
            print(f"preview tags = {tags}")
            tags = sorted(tags)
            print(f"sortedTags = {tags}")
            for tag in tags:
                index = self._bisect(oldtags,tag)
                print(f"index = {index}")
                if index == -1:
                    newtags.append(tag)
            for i,oldtag in enumerate(oldtags):
                index = self._bisect(tags, oldtag)
                if index == -1:
                    disposableids.append(oldids[i])
            for trash in disposableids:
                query = """DELETE FROM evento_etiqueta WHERE idEvento = %s AND idEtiqueta = %s"""
                cursor.execute(query, (id,trash))
            self._associate_tags(cursor=cursor, idEvent=id, tags=newtags)
        self._conection.commit()
        cursor.close()
        self._conection.close()
        self._events_for_month()
        self._classify_events_by_day()
    
    def delete_event(self, idEvent):
        self.connectBD()

        cursor = self._conection.cursor()

        query = """DELETE FROM evento_etiqueta
        WHERE idEvento = %s"""

        cursor.execute(query, (idEvent, ))

        query = """DELETE FROM eventos
        WHERE idEvento = %s"""

        cursor.execute(query, (idEvent, ))
        self._conection.commit()

        cursor.close()
        self._conection.close()
        self._events_for_month()
        self._classify_events_by_day()



"""cronos = Datos("root", "ACL&cag20", "localhost","cronosdb")
cronos.modifyevent(50,"estudiar programacion2", 200, datetime.today(), datetime(2023,7,2,0,0,0,0), "DEBES ESTUDIAR", 1, ("no procastines","programacion 2"))
for x in cronos.eventsbyday[6]:
    print(x)
    """
