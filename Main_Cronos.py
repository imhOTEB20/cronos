#Ventana Principal
import tkinter as tk
from tkinter import ttk

from datetime import datetime

from Logo import Logo
from Reloj import Reloj
from DateGrid import DateGrid

import mysql.connector

class MainCronos(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._frame = ttk.Frame(self)
        self._frame.grid(row=0, column=0)
        self._logo = Logo(self._frame)
        self._logo.grid(row=0,column=0)
        
        self._clock = Reloj(self._frame)
        self._clock.grid(row=0, column=1)

        self._dateGrid = DateGrid(self, self.load_events)
        self._dateGrid.grid(row=1, column=0)
        
        self._title_list = tk.StringVar()
        self_label_list = ttk.Label(self, textvariable=self._title_list)
        self_label_list.grid(row=2, column=0)
        self._list_day_events = tk.Listbox(self, width=40)
        self._list_day_events.grid(row=3, column=0)
        self.load_events()

        self._establish_conection()
    
    @staticmethod
    def _establish_conection():
        conection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "ACL&cag20",
            database = "cronosdb")
        return conection
    
    def load_events(self, date:datetime = None):
        if date!=None and (self._clock.today.day!=date.day or self._clock.today.month!=date.month or self._clock.today.year!=date.year):
            self._title_list.set(f"{self._clock._day_name[date.weekday()]} {date.day}")
            date_str = date.strftime('%Y-%m-%d')
        else:
            self._title_list.set('HOY')
            date_str = self._clock.today.strftime('%Y-%m-%d')
        
        self._list_day_events.delete(0, tk.END)
        conection = self._establish_conection()
        query = """SELECT titulo,fecha_y_hora_e FROM eventos WHERE DATE(eventos.fecha_y_hora_e) = %s"""
        cursor = conection.cursor()
        cursor.execute(query, (date_str,))
        result = cursor.fetchall()
        if not result:
            self._list_day_events.insert(tk.END, "No hay eventos en este dia.")
        else:
            for evento in result:
                hora = evento[1].strftime('%H:%M')
                self._list_day_events.insert(tk.END, f"{hora} - {evento[0]}")
        conection.close()

    def charge_eventos(self):
        connection = self._establish_conection()
        cursor = connection.cursor()
        date = self._dateGrid._date
        consulta = """SELECT """
root = tk.Tk()
app = MainCronos(root)
app.grid(padx=3,pady=3)
root.mainloop()
