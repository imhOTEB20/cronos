#Ventana Principal
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from datetime import datetime
from time import sleep

from Logo import Logo
from Reloj import Reloj
from DateGrid import DateGrid
from VentanaDetalles import Form
from DataBase import Datos
from CenteredTopLevel import CenteredTopLevel

class MainCronos(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent
        self._frame = ttk.Frame(self)
        self._frame.grid(row=0, column=0)
        self._logo = Logo(self._frame)
        self._logo.grid(row=0,column=0)
        
        self._clock = Reloj(self._frame)
        self._clock.grid(row=0, column=1)
        self.bind("<Destroy>", self._if_im_destroyed)

        self._dateGrid = DateGrid(self, self.load_events)
        self._dateGrid.grid(row=1, column=0)

        self._db = Datos(user='root', password='ACL&cag20', host='localhost', database='cronosdb')
        
        self._title_list = tk.StringVar()
        self_label_list = ttk.Label(self, textvariable=self._title_list)
        self_label_list.grid(row=2, column=0)
        self._list_day_events = tk.Listbox(self, width=40, selectmode=tk.SINGLE)
        self._list_day_events.grid(row=3, column=0)
        self._list_day_events.bind('<Double-Button-1>', self._on_double_click_in_event)
        self.load_events()

        self._buttons_frame = ttk.Frame(self)
        self._buttons_frame.grid(row= 4, column=0)
        ttk.Button(self._buttons_frame, text='Agregar Evento',
                   command=self._button_action_to_add_event
                   ).grid(row= 0, column= 0)
        ttk.Button(self._buttons_frame, text='Eliminar Evento',
                   command=self._button_action_to_delete_event
                   ).grid(row= 0, column= 1)
    
    def _if_im_destroyed(self, event):
        self._clock.flag = False
        sleep(0.01)
    
    def _button_action_to_delete_event(self):
        index = self._list_day_events.curselection()[0]
        evento = self._list_day_events.get(index)
        if messagebox.askyesno('Eliminar Evento',
                                  f'Esta seguro de eliminar {evento}'):
            self._db.delete_event(self._db.eventsbyday[self._day][index][0])        
            self.reset_list()
    
    def _button_action_to_add_event(self):
        addEvento = CenteredTopLevel(self, self._parent)
        addEvento.title("Agregar Evento")
        Form(addEvento, None, self._db.new_event, self.reset_list)
        self.reset_list()
    
    def _on_double_click_in_event(self, event):
        index  = self._list_day_events.curselection()[0]
        if self._list_day_events.get(index) != "NO HAY EVENTO ESTE DIA.":
            list = self._db.eventsbyday[self._day][index]
            eventData = {"id": list[0],
                         "title": list[1],
                         "duration": list[2],
                         "datetimeE": list[3],
                         "datetimeR": list[4],
                         "detail": list[5],
                         "relevance": list[6],
                         "tags": self._db.tags_cross_idEvent(list[0])}
            editEvento = CenteredTopLevel(self, self._parent)
            editEvento.title("Editar Evento")
            Form(editEvento, eventData, self._db.modifyevent, self.reset_list)

    def reset_list(self):
        self._list_day_events.delete(0, tk.END)
        try:
            for event in self._db.eventsbyday[self._day]:
                self._list_day_events.insert(tk.END, event[1])
        except KeyError as error:
            self._list_day_events.insert(tk.END, "NO HAY EVENTO ESTE DIA.")

    def load_events(self, date:datetime = None):
        if date!=None and (self._clock.today.day!=date.day or self._clock.today.month!=date.month or self._clock.today.year!=date.year):
            self._title_list.set(f"{self._clock._day_name[date.weekday()]} {date.day}")
            self._day = date.day
            if self._db.date.month!=date.month or self._db.date.year!=date.year:
                self._db.date = date
        else:
            self._title_list.set('HOY')
            self._day = self._clock.today.day
        self.reset_list()


def on_closing():
    if messagebox.askokcancel("Salir", "¿Seguro que deseas salir?"):
        root.destroy()

root = tk.Tk()
app = MainCronos(root)
app.grid(padx=3,pady=3)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
