import tkinter as tk

class Tag(tk.Label):
    tag_list = []
    def __init__(self, parent, text, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(text=text, bg='lightgray', padx=5, pady=5, anchor='sw', justify='left')
        self._config_cross_button()
        self.tag_list.append(text)
        self._text = text
    
    def _config_cross_button(self):
        x_icon = "\u2716"
        self._close_label = tk.Label(self, text=x_icon, font=("Arial", 1), bg='red', fg='white', padx=3, pady=3)
        self._close_label.place(relx=1.0, rely=0.0, anchor='ne')
        self._close_label.bind("<Button-1>", lambda event: self._destroyTag(event))
    
    def _destroyTag(self, event):
        self.tag_list.remove(self._text)
        print(self.tag_list)
        self.destroy()
