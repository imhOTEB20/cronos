import tkinter as tk
from tkinter import ttk

from datetime import datetime

#Por favor, instalar la fuente de texto que se encuentra en ds_digital
class Time(ttk.Frame):
    
    def __init__(self, parent, dt:datetime, extra_function=None):
        super().__init__(parent)
        self._parent = parent
        self._extra_function = extra_function
        self._tuple_font_label = ("DS-Digital", 24)
        self._tuple_font_buttons = ("Arial", 12)
        self._datetime = dt
        self._config_frame()
    
    def _config_frame(self):
        self._widget_frame = ttk.Frame(self)
        self._widget_frame.grid(row=0, column=0)
        self._config_label()
        self._config_buttons()

    def _config_label(self):
        self._hora_text = tk.StringVar()
        hour = self._datetime.hour
        if hour < 10:
            hour = f"0{hour}"
        self._hora_text.set(hour)
        tk.Label(self._widget_frame,
                 textvariable=self._hora_text,
                 pady=1,
                 font=self._tuple_font_label
                 ).grid(row= 1, column= 0)
        tk.Label(self._widget_frame,
                 text = ":",
                 pady=1,
                 font=self._tuple_font_label
                 ).grid(row= 1, column= 1)
        self._minute_text = tk.StringVar()
        minute = self._datetime.minute
        if minute < 10:
            minute = f"0{minute}"
        self._minute_text.set(minute)
        tk.Label(self._widget_frame,
                 textvariable=self._minute_text,
                 pady=1,
                 font=self._tuple_font_label
                 ).grid(row= 1, column= 2)
    
    def _config_buttons(self):
        time = ttk.Frame
        #Botones de arriba
        ttk.Button(self._widget_frame, text="🔼", command= lambda value=True: self._action_button_hour(True)).grid(row= 0, column= 0)
        ttk.Button(self._widget_frame, text="🔼", command= lambda value=True: self._action_button_minute(value)).grid(row= 0, column= 2)
        #Botones de abajo
        ttk.Button(self._widget_frame, text="🔽", command= self._action_button_hour).grid(row= 2, column= 0)
        ttk.Button(self._widget_frame, text="🔽", command= self._action_button_minute).grid(row= 2, column= 2)
        #Boton de Aceptar
        acccept_frame = ttk.Frame(self, padding=5)
        acccept_frame.grid(row=1,column=0)
        ttk.Button(acccept_frame, text="Aceptar", command= self._action_button_accept).grid(row=0, column=0)
    
    def _action_button_hour(self, upButton=False):
        if upButton:
            hour = int(self._hora_text.get()) + 1
            if hour < 24:
                if hour < 10:
                    hour = f"0{hour}"
                self._hora_text.set(hour)
            else:
                self._hora_text.set("00")
        else:
            hour = int(self._hora_text.get()) - 1
            if hour > -1:
                if hour < 10:
                    hour = f"0{hour}"
                self._hora_text.set(hour)
            else:
                self._hora_text.set("23") 

    def _action_button_minute(self, upButton=False):
        if upButton:
            minute = int(self._minute_text.get()) + 1
            if minute < 60:
                if minute < 10:
                    minute = f"0{minute}"
                self._minute_text.set(minute)
            else:
                self._minute_text.set("00")
        else:
            minute = int(self._minute_text.get()) - 1
            if minute > -1:
                if minute < 10:
                    minute = f"0{minute}"
                self._minute_text.set(minute)
            else:
                self._minute_text.set("59")

    def _action_button_accept(self):
        self._time = f"{self._hora_text.get()}:{self._minute_text.get()}"
        if self._extra_function != None:
            self._extra_function(self._time)
        self._parent.destroy()                  


"""def functionExample(time):
    print(time)
root = tk.Tk()
app = Time(root, datetime.today(), functionExample)
app.grid()
root.mainloop()"""