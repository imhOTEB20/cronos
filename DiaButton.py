#dia_button
import tkinter as tk
from tkinter import ttk

import datetime

import mysql.connector

class DiaButton(ttk.Button):
    def __init__(self, parent, date: datetime, listbox: tk.Listbox):
        super().__init__(parent)
        self._parent = parent
        self._listbox = listbox
        self._loadDate(date)

        self.config(command=self.action_button)
        self.config(text=str(date.day))
    
    def _loadDate(self, date:datetime):
        self._strDate = f"{date.year}-{date.month}-{date.day}"

    def action_button(self):
        try:
            #conexion a la base de datos
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ACL&cag20",
                datebase="evenetosDB"
            )
            cursor = connection.cursor()

            #Hacemos una consulta para obtener los eventos que tengan la fecha 
            consulta = f"SELECT titulo FROM eventos WHERE fecha_evento = {self._strDate}"
            cursor.execute(consulta)
            eventos = cursor.fetchall()

            self._listbox.delete(0, tk.END)
            for evento in eventos:
                self._listbox.insert(tk.END, evento[0])
            
            cursor.close()
            connection.close()
        except mysql.connector.Error as error:
            print("Error al conectarse a la base de datos: ", error)