#cargador de fecha
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

from datetime import datetime
from calendar import monthrange

class DateGrid(ttk.Frame):
    def __init__(self, parent, extra_day_action=None, tiny:bool=False):
        super().__init__(parent)
        #configura modo chiquito:
        self._tiny = tiny
        if self._tiny:
            self._tuple_font = ("Arial",7)
        else:
            self._tuple_font = ("Arial", 10)
        #cargar fecha actual
        self._date = datetime.now()
        #cargar marco
        self._frame = ttk.Frame(self)
        self._frame.grid()
        self._extra_day_action = extra_day_action
        self._ttk_charger()
    
    def _days_charger(self):
        day_name, days = monthrange(self._date.year, self._date.month)
        
        day_name_list = ["LU","MA","MI","JU","VI","SA","DO"]
        
        for index,header in enumerate(day_name_list):
            ttk.Label(self._days_grid, text=header, font=self._tuple_font).grid(row=0,column=index)
        
        row = 1
        for day in range(1,days+1):
            button = tk.Button(self._days_grid,
                       text=str(day),
                       width=3,
                       font=self._tuple_font,
                       command=lambda day_num=day: self._action_day_button(day_num)
                       )
            button.grid(row=row, column=day_name)
            if self._tiny:
                button.configure(width=2)

            if day_name != 6:
                day_name += 1
            else:
                row += 1
                day_name = 0
    
    def _action_day_button(self, day):
        self._date = datetime(self._date.year, self._date.month, day)
        if self._extra_day_action != None:
            self._extra_day_action(self._date)
    
    def _ttk_charger(self):
         #cargar ttks
        self._setting_year_button()

        self._month_name_list = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        self._month_button = ttk.Button(self._frame,
                                        text=self._month_name_list[self._date.month - 1],
                                        command=self._month_charger)
        print(self._date.month)
        self._month_button.grid(row=1, sticky="ew")

        self._days_grid = ttk.Frame(self._frame)
        self._days_grid.grid(row=2)

        self._days_charger()
    
    def _month_charger(self):
        #recargar marco
        self._recreate_frame()
        #cargar boton año
        self._setting_year_button()
        #cargar meses
        row=0
        column=0
            #cargar cuadricula de meses
        self._month_grid = ttk.Frame(self._frame)
        self._month_grid.grid(row=1)
        for month_num in range(0,12):
            ttk.Button(self._month_grid,
                       text=self._month_name_list[month_num],
                       command=lambda month=month_num+1: self._action_month_button(month)
                       ).grid(row=row,column=column)
            if column!=2:
                column+=1
            else:
                row+=1
                column=0
    
    def _action_month_button(self, month_num):
        self._date = datetime(self._date.year,month_num,self._date.day)
        #recargar marco
        self._recreate_frame()
        self._ttk_charger()

    
    def _setting_year_button(self):
        self._year_button = ttk.Button(self._frame,
                                       text=str(self._date.year),
                                       command=lambda year=self._date.year: self.year_charger(year))
        self._year_button.grid(row=0, sticky="ew")
    
    def _recreate_frame(self):
        #eliminar_marco
        self._frame.destroy()
        #cargar marco
        self._frame = ttk.Frame(self)
        self._frame.grid()
    
    def year_charger(self, year):
        #recargar marco
        self._recreate_frame()
        #cargar encabezado
        lowest_year_range = year - 4
        highest_year_rank = year + 4
        header = ttk.Frame(self._frame)
        header.grid(row=0)
        ttk.Label(header, text = f"{lowest_year_range}-{highest_year_rank}").grid(row=0,column=0, sticky="ew")
        ttk.Button(header, text="<<", command=lambda year=lowest_year_range - 5: self.year_charger(year)).grid(row=0,column=1)
        ttk.Button(header, text=">>", command=lambda year=highest_year_rank + 5: self.year_charger(year)).grid(row=0,column=2)
        #cargar botones de anios
        years_grid = ttk.Frame(self._frame)
        years_grid.grid(row=1)

        row = 0
        column = 0
        for anio in range(lowest_year_range, highest_year_rank+1):
            ttk.Button(years_grid, text=str(anio), command=lambda year=anio: self._action_year_button(year)).grid(row=row, column=column)
            if column != 2:
                column+=1
            else:
                column=0
                row+=1
    
    def _action_year_button(self, year):
        #cambiar año del datetime en self._date
        self._date = datetime(year, self._date.month, self._date.day)
        #cargar mes
        self._month_charger()
"""
root = tk.Tk()
def prueba(date:datetime):
    print(f'TODO OK {date.strftime("%Y-%m-%d")}')
app = DateGrid(root, prueba, tiny= True)
app.grid()
root.mainloop()"""
