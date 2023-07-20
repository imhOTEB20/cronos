import tkinter as tk

class CenteredTopLevel(tk.Toplevel):
    def __init__(self, parent, root):
        super().__init__(parent)
        self.parent = parent
        self._configure_position(root)
        self.transient(parent)
        self.grab_set()
        

    def _configure_position(self, root:tk.Tk):
        self.parent.update_idletasks()
        width_root = root.winfo_width()
        height_root = root.winfo_height()
        x_root = root.winfo_x()
        y_root = root.winfo_y()
        x = (x_root + width_root // 2) - self.winfo_width() // 2
        y = (y_root + height_root // 2) - self.winfo_height() // 2
        self.geometry(f"+{x}+{y}")
        