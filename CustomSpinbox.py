#from: https://github.com/CodeSame/ctkSpinbox

import customtkinter as ctk
from CTkToolTip import *
from typing import Callable

import customtkinter as ctk
from CTkToolTip import *
from typing import Callable

class CustomSpinbox(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: int = 1,
                 min_value: int = 0, 
                 max_value: int = 100,
                 command: Callable = None,
                 **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  

        self.grid_columnconfigure((0, 2), weight=0)  
        self.grid_columnconfigure(1, weight=1)  

        self.subtract_button = ctk.CTkButton(self, text="-", width=height-6, height=height-6, fg_color="transparent", command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = ctk.CTkEntry(self, width=width - 70, height=height - 6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="nsew")
        
        self.add_button = ctk.CTkButton(self, text="+", width=height-6, height=height-6, fg_color="transparent", command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)
    
        # default value
        self.entry.insert(0, "0")
        # Bind mouse wheel events
        self.entry.bind("<MouseWheel>", self.on_mouse_wheel)
        self.subtract_button.bind("<MouseWheel>", self.on_mouse_wheel)
        self.add_button.bind("<MouseWheel>", self.on_mouse_wheel)
        self.bind("<MouseWheel>", self.on_mouse_wheel)
        
        # Aggiungi il tooltip e forza la finestra a essere temporaneamente in primo piano
        self.set_tooltip()

    def set_tooltip(self):
        CTkToolTip(self.entry, message="Use the mouse wheel to adjust the value")
        # Forza la finestra a essere in primo piano solo per un breve periodo
        parent_window = self.winfo_toplevel()  # Ottieni la finestra Toplevel
        parent_window.attributes('-topmost', True)
        parent_window.after(500, lambda: parent_window.attributes('-topmost', False))

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) + self.step_size
            if value <= self.max_value: 
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
        except ValueError:
            return
    
    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) - self.step_size
            if value >= self.min_value: 
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> int:
        try:
            return int(self.entry.get())
        except ValueError:
            return 0
            
    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.add_button_callback()
        else:
            self.subtract_button_callback()
            
    def set(self, value: int):
        self.entry.delete(0, "end")
        self.entry.insert(0, int(value))