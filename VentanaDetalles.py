#Ventana con dellates del evento
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

#import mysql.connector

from datetime import datetime
from random import randint

from ToolTip import ToolTip
from DateGrid import DateGrid
from Time import Time
from CenteredTopLevel import CenteredTopLevel
from Tag import Tag

class Form(ttk.Frame):
    """Marco que contiene el formulario para crear o editar un evento."""
    def __init__(self, parent, data=None):
        self._parent = parent
        """data:  {title:'titulo del evento',
                    detail: 'detalles del event',
                    datetimeE: 'fecha y hora del evento',
                    datetimeR: 'fecha y hora del recordatorio',
                    duration: 'duracion del evento',
                    relevance: 'importancia del evento -> normal = 0, importante = 1',
                    tags: 'tupla con etiquetas del evento'}"""
        super().__init__(parent, padding = 3)
        super().grid()
        self._data = data
        #configuracion de los widgets de la ventana
        self._config_witget()

    def _config_witget(self):
        self._row = 0
        self._config_title()
        self._config_detail()
        self._config_duration()
        self._config_datetimeE()
        self._config_datetimeR()
        self._config_relevance()
        self._config_tags()
        self._config_buttons_confirm()
    
    def _next_row(self):
        self._row += 1

    def _config_title(self):
        #configurar titulo, su line de text, y el contador de caracteres
        ttk.Label(self, text = "Titulo", padding = 3).grid(row = self._row, column = 0)
        self._strvar_title = tk.StringVar()
        self._next_row()
        ttk.Entry(self, textvariable = self._strvar_title, validate = "key",
                  validatecommand=(self.register(self._title_character_counter), '%P')
                  ).grid(sticky='nsew', row = self._row, column= 0)
        if self._data != None:
            self._strvar_title.set(self._data['title'])
        title_count_frame = ttk.Frame(self)
        self._next_row()
        title_count_frame.grid(row = self._row, column=0)
        self._title_char_counter = tk.StringVar()
        self._title_char_counter.set("0/45")
        ttk.Label(title_count_frame,width=9).grid(row = 0, column = 0)
        ttk.Label(title_count_frame,width=9).grid(row = 0, column = 1)
        ttk.Label(title_count_frame, textvariable=self._title_char_counter).grid(row = 0, column = 2)
    
    def _config_detail(self):
        #configuracion de detalles, su campo de texto, y el contador de caracteres
        self._next_row()
        ttk.Label(self, text = "Detalles", padding = 3).grid(row = self._row, column = 0)
        self._detail_text = tk.Text(self, width = 20, height=5)
        if self._data != None:
            if self._data['detail'] != None:
                self._detail_text.insert('1.0', self._data['detail'])
        self._next_row()
        self._detail_text.grid(row=self._row, column=0, sticky='nsew')
        self._detail_text.bind("<KeyRelease>", self._detail_character_counter)
        count_frame = ttk.Frame(self)
        self._next_row()
        count_frame.grid(row = self._row, column=0)
        self._char_counter = tk.StringVar()
        self._char_counter.set("0/100")
        ttk.Label(count_frame,width=9).grid(row = 0, column = 0)
        ttk.Label(count_frame,width=9).grid(row = 0, column = 1)
        ttk.Label(count_frame, textvariable=self._char_counter).grid(row = 0, column = 2)
    
    def _config_duration(self):
        #configuracion de la duracion, su linea de texto, controlador de caracteres
        self._next_row()
        ttk.Label(self, text = 'Duracion').grid(row = self._row, column=0)
        self._next_row()
        self._duration_spinbox = ttk.Spinbox(self, from_= 0, to = 120,
                                             justify='center',
                                             validate = 'key',
                                             )
        self._duration_spinbox.grid(row= self._row, column= 0)
        if self._data != None:
            self._duration_spinbox.set(self._data['duration'])
        else:
            self._duration_spinbox.set(60)
        ToolTip(self._duration_spinbox, "duracion en min. de 0 a 120 inclusive.")
    
    def _config_datetimeE(self):
        self._next_row()
        ttk.Label(self, text= "Fecha y Hora del Evento").grid(row= self._row, column=0)
        self._next_row()
        datetimeE_frame = ttk.Frame(self)
        datetimeE_frame.grid(row= self._row, column=0)
        if self._data != None:
            self._dayE = self._data['datetimeE']
        else:
            self._dayE = datetime.today()
        dateE = self._dayE.strftime('%d-%m-%Y')
        timeE = self._dayE.strftime('%H:%M')
        self._dateE_Button = ttk.Button(datetimeE_frame, text= dateE, command=self._action_button_date)
        self._dateE_Button.grid(row= 0, column= 0)
        self._timeE_Button = ttk.Button(datetimeE_frame, text= timeE, command= self._action_button_time)
        self._timeE_Button.grid(row= 0, column= 1)
    
    def _config_datetimeR(self):
        self._next_row()
        ttk.Label(self, text= "Fecha y Hora Recordatorio").grid(row= self._row, column=0)
        self._next_row()
        datetimeR_frame = ttk.Frame(self)
        datetimeR_frame.grid(row= self._row, column=0)
        if self._data != None:
            self._dayR = self._data['datetimeR']
        else:
            self._dayR = datetime.today()
        dateR = self._dayR.strftime('%d-%m-%Y')
        timeR = self._dayR.strftime('%H:%M')
        self._dateR_Button = ttk.Button(datetimeR_frame, text=dateR, command= lambda value=True: self._action_button_date(value))
        self._dateR_Button.grid(row= 0, column= 0)
        self._timeR_Button = ttk.Button(datetimeR_frame, text= timeR, command= lambda value=True: self._action_button_time(value))
        self._timeR_Button.grid(row= 0, column= 1)
    
    def _config_relevance(self):
        self._next_row()
        relevance_frame = ttk.Frame(self)
        relevance_frame.grid(row= self._row, column=0)
        ttk.Label(relevance_frame, text= 'Relevancia: ').grid(row= 0, column= 0)
        options = ['normal', 'importante']
        option = tk.StringVar()
        if self._data != None:
            option.set(self._data['relevance'])
        else:
            option.set('normal')
        ttk.OptionMenu(relevance_frame, option, option.get(), *options).grid(row= 0, column= 1)
    
    def _config_buttons_confirm(self):
        self._next_row()
        frame_confirm = ttk.Frame(self)
        frame_confirm.grid(row= self._row, column=0)
        ttk.Button(frame_confirm, text= "Aceptar", command=self._action_button_accept).grid(row= 0, column= 0)
        ttk.Button(frame_confirm, text= "Cancelar", command=self._action_button_close).grid(row= 0, column= 1)
    
    def _config_tags(self):
        self._next_row()
        self._frame_tags = ttk.Frame(self)
        self._frame_tags.grid(row=self._row, column=0)
        if self._data != None:
            for tag in self._data['tags']:
                Tag(self._frame_tags, text=tag).pack(side='left')
        self._next_row()
        tag_input_frame = ttk.Frame(self)
        tag_input_frame.grid(row= self._row)
        self._tag_row = 0
        self._tag_col = 0
        ttk.Label(tag_input_frame, text="tag:").grid(row=0,column=0)
        self._stringtag = tk.StringVar()
        ttk.Entry(tag_input_frame, textvariable=self._stringtag).grid(row= 0, column= 1)
        ttk.Button(tag_input_frame, text= 'Agregar',
                   command=self._action_button_addtag
                   ).grid(row= 0, column= 2)
    
    def _action_button_addtag(self):
        tag = self._stringtag.get()
        if tag != "":
            if not(tag in Tag.tag_list):
                Tag(self._frame_tags, text=tag).pack(side='left')
    
    def _congruent_data(self):
        self._title_ok = self._strvar_title.get() != ""
        try:
            duration = int(self._duration_spinbox.get())
            self._duration_ok = duration > -1 and duration < 121
        except ValueError as error:
            self._duration_ok = False
        dateE = datetime.strptime(f"{self._dateE_Button['text']} {self._timeE_Button['text']}:00",
                                  '%d-%m-%Y %H:%M:%S')
        dateR = datetime.strptime(f"{self._dateR_Button['text']} {self._timeR_Button['text']}:00",
                                  '%d-%m-%Y %H:%M:%S')
        self._datetime_ok = dateE >= dateR
        return self._title_ok and self._duration_ok and self._datetime_ok
    
    def _action_button_accept(self):
        if self._congruent_data():
            pass
        else:
            if not(self._title_ok):
                messagebox.showerror('Error Titulo', "El titulo del evento no puede estar vacio.")
            elif not(self._duration_ok):
                try:
                    duration = int(self._duration_spinbox.get())
                    if duration < 0 or duration > 120:
                        messagebox.showerror('Error Duracion', "La duracion no puede ser negativa o mayor a 2 horas.")
                except ValueError as error:
                    messagebox.showerror("Error Duracion", "La duracion debe ser un numero entero.")
            elif not(self._datetime_ok):
                messagebox.showerror('Error fecha y hora de recordatorio', 'La fecha y hora del recordatorio no puede ser posterior a la fecha del Evento.')
    
    def _action_button_close(self):
        resultado = messagebox.askyesno("Confirmacion", '¿Esta seguro de cancelar la creacion del evento?')
        if resultado:
            self._parent.destroy()
    
    def _select_dateE(self, dt:datetime):
        self._dateE_Button.config(text= dt.strftime('%d-%m-%Y'))
        self._topLevel.destroy()
    
    def _select_dateR(self, dt:datetime):
        self._dateR_Button.config(text= dt.strftime('%d-%m-%Y'))
        self._topLevel.destroy()
    
    def _select_timeE(self, time:str):
        self._timeE_Button.config(text= time)
    
    def _select_timeR(self, time:str):
        self._timeR_Button.config(text= time)

    def _action_button_date(self, rightButton=False):
        self._topLevel = CenteredTopLevel(self, self._parent)
        self._topLevel.title("Calentario")
        if rightButton:
            date = DateGrid(self._topLevel, self._select_dateR,True)
        else:
            date = DateGrid(self._topLevel, self._select_dateE,True)
        date.grid()
    
    def _action_button_time(self, rightButton=False):
        self._topLevel = CenteredTopLevel(self, self._parent)
        self._topLevel.title("Configurar Hora")
        
        if rightButton:
            time =Time(self._topLevel, self._dayR, self._select_timeR)
        else:
            time =Time(self._topLevel, self._dayE, self._select_timeE)
        time.grid()
        
    def _title_character_counter(self,text):
        if len(text) > 45:
            return False
        else:
            self._title_char_counter.set(f"{len(text)}/45")
        return True

    def _detail_character_counter(self,event):
        text = self._detail_text.get("1.0", "end-1c")
        if len(text) < 101:
            self._char_counter.set(f"{len(text)}/100")
        else:
            self._detail_text.delete("end-2c", "end-1c")


        


root = tk.Tk()
form = Form(parent=root)
root.mainloop()