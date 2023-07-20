#Reloj
#Frame que contiene lo necesario para el funcionamiento del reloj del main
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

from datetime import datetime
from time import sleep

import threading

class Reloj(ttk.Frame):
    """La clase Reloj, es un frame que muestra en tiempo real, la fecha y la hora actual"""
    def __init__(self, parent):
        super().__init__(parent)
        self._clock_string = tk.StringVar()
        self._date_string = tk.StringVar()

        self._day_name = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
        self._month_name = ["","Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

        self._setting_frame()

    def _setting_frame(self):
        #Hilo del reloj
        self._clock_thread = threading.Thread(target=self._clock_update, name="clock threand")
        self._clock_thread.start()
        #Configuraciones necesarias para mostrar la hora actual
        
        self._clock_font = tkFont.Font(family="Cooper Negra", size=25)
        self._clock_label = ttk.Label(self, textvariable=self._clock_string, font=self._clock_font)
        self._clock_label.grid(row=0)
        #Configuraciones necesarias para mostrar la fecha actual
        self._date_font = tkFont.Font(family="Arial", size=7)
        self._date_label = ttk.Label(self, textvariable=self._date_string, font=self._date_font)
        self._date_label.grid(row=1)
    
    def _clock_update(self):
        #funcion que actualiza el texto de los label de fecha y hora
        while True:
            self.today = datetime.today()
            if self.today.hour>9:
                if self.today.minute>9:
                    if self.today.second>9:
                        hour_text = f"{self.today.hour}:{self.today.minute}:{self.today.second}"
                    else:
                        hour_text = f"{self.today.hour}:{self.today.minute}:0{self.today.second}"
                else:
                    if self.today.second>9:
                        hour_text = f"{self.today.hour}:0{self.today.minute}:{self.today.second}"
                    else:
                        hour_text = f"{self.today.hour}:0{self.today.minute}:0{self.today.second}"
            else:
                if self.today.minute>9:
                    if self.today.second>9:
                        hour_text = f"0{self.today.hour}:{self.today.minute}:{self.today.second}"
                    else:
                        hour_text = f"0{self.today.hour}:{self.today.minute}:0{self.today.second}"
                else:
                    if self.today.second>9:
                        hour_text = f"0{self.today.hour}:0{self.today.minute}:{self.today.second}"
                    else:
                        hour_text = f"0{self.today.hour}:0{self.today.minute}:0{self.today.second}"
            fecha_text = f"{self._day_name[self.today.weekday()]} {self.today.day}, de {self._month_name[self.today.month]} de {self.today.year}"
            self._clock_string.set(hour_text)
            self._date_string.set(fecha_text)
            sleep(1)

"""
root = tk.Tk()
app = Reloj(root)
app.grid()
root.mainloop()
"""