#Logo
#Frame que contiene lo necesario para mostrar el logo "cronos"
import tkinter as tk
from tkinter import ttk

class Logo(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._logo = tk.PhotoImage(file="Logo.png")

        self._setting_frame()
    
    def _setting_frame(self):
        self._imagen_label = ttk.Label(self, image=self._logo)
        self._imagen_label.grid()

"""
root = tk.Tk()
app = Logo(root)
app.grid()
root.mainloop()
"""