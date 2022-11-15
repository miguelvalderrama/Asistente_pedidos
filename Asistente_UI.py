import tkinter
import tkinter.messagebox
import json
import pandas as pd
import customtkinter
import farmacias
import os
import datetime
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox



customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):

    WIDTH = 1080
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        self.title("Comparador de precios")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        with open("temp/config.json", "r") as f:
            self.fconfig = json.load(f)
            self.ultima_actualizacion = self.fconfig["last_update"]

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Barra de herramientas",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Actualizar Archivos",
                                                command=self.actualizar_archivos)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Nuevo Pedido",
                                                command="")
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Descargar Archivos",
                                                command="")
        self.button_3.grid(row=4, column=0, pady=10, padx=20)

        self.label_last_update = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Ultima actualización: \n" + self.ultima_actualizacion,
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_last_update.grid(row=8, column=0, pady=10, padx=10)

        self.button_4 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Configuración",
                                                command=self.config)
        self.button_4.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (1x2)
        self.frame_right.grid_rowconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure((0,1), weight=1)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right,
                                                    corner_radius=6)
        self.frame_info.grid(row=0, column=0, columnspan=2, pady=10, padx=20, sticky="nsew")

        # configure grid layout (2x4)
        self.frame_info.grid_rowconfigure(0, weight=1)
        self.frame_info.grid_columnconfigure(0, weight=1)

        # Read farmacias.json config file
        with open("farmacias.json", "r") as f:
            self.farmacias = json.load(f)
        
        # Get farmacias names and their state (Activo/Inactivo)
        self.farmacias_names = []
        self.farmacias_state = []
        self.farmacias_abrev = []
        for farmacia in self.farmacias:
            self.farmacias_names.append(self.farmacias[farmacia]["nombre"])
            self.farmacias_state.append(self.farmacias[farmacia]["estado"])
            self.farmacias_abrev.append(self.farmacias[farmacia]["abreviatura"])

        # List for farmacias activas
        self.farmacias_activas = []
        self.farmacias_activas_abrev = []
        for i in range(len(self.farmacias_state)):
            if self.farmacias_state[i] == "Activo":
                self.farmacias_activas.append(self.farmacias_names[i])
                self.farmacias_activas_abrev.append(self.farmacias_abrev[i])

        # Insert treeview
        self.tree = ttk.Treeview(self.frame_info, columns=('Descripcion', 'Precio', 'Drogueria', self.farmacias_activas_abrev[0], self.farmacias_activas_abrev[1], self.farmacias_activas_abrev[2]), show='headings')
        self.tree.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Insert scrollbar
        self.scrollbar = customtkinter.CTkScrollbar(self.frame_info, command=self.tree.yview)
        self.scrollbar.grid(row=0, column=2, sticky="ns")
        
        # Configure treeview
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.tree.heading('Descripcion', text='Descripcion')
        self.tree.heading('Precio', text='Precio')
        self.tree.heading('Drogueria', text='Drogueria')
        self.tree.heading(self.farmacias_activas_abrev[0], text=self.farmacias_activas_abrev[0])
        self.tree.heading(self.farmacias_activas_abrev[1], text=self.farmacias_activas_abrev[1])
        self.tree.heading(self.farmacias_activas_abrev[2], text=self.farmacias_activas_abrev[2])
        self.tree.column('Descripcion', width=300, anchor='center')
        self.tree.column('Precio', width=100, anchor='center')
        self.tree.column('Drogueria', width=150, anchor='center')
        self.tree.column(self.farmacias_activas_abrev[0], width=50, anchor='center')
        self.tree.column(self.farmacias_activas_abrev[1], width=50, anchor='center')
        self.tree.column(self.farmacias_activas_abrev[2], width=50, anchor='center')

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Busqueda",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command="")
        self.button_5.grid(row=2, column=1, columnspan=1, rowspan=2,  pady=10, padx=20, sticky="we")

        self.entry_1 = customtkinter.CTkEntry(master=self.frame_right,
                                                placeholder_text="Buscar",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None)  # <- no fg_color
        self.entry_1.grid(row=2, column=0, columnspan=1, rowspan=2,  pady=10, padx=20, sticky="we")

        # set default values
        self.button_2.configure(state="disabled", text="Nuevo Pedido")
        self.button_3.configure(state="disabled", text="Descargar Archivos")
        self.entry_1.bind("<Return>", lambda event: print("Return pressed"))
        self.tree.bind("<Double-1>", self.change_units)
        
        # Full size window
        self.state("zoomed")

    def change_units(self, event):
        """Change the number of units of the product for each farmacia"""
        item = self.tree.selection()[0]
        values = self.tree.item(item, "values")
        # Create a new window
        self.new_window = customtkinter.CTkToplevel(self)
        self.new_window.title("Cambiar Unidades")
        self.new_window.geometry("100x200")
        self.new_window.maxsize(1000, 200)
        self.new_window.minsize(1000, 200)
        self.new_window.update_idletasks()
        # Center window on screen
        x = (self.new_window.winfo_screenwidth() // 2) - (self.new_window.winfo_width() // 2)
        y = (self.new_window.winfo_screenheight() // 2) - (self.new_window.winfo_height() // 2)
        self.new_window.geometry("+{}+{}".format(x-380, y))

        self.new_window.grid_rowconfigure((0,1,2), weight=1)
        self.new_window.grid_columnconfigure((0,1,2), weight=1)

        self.labels_frame = customtkinter.CTkFrame(master=self.new_window,
                                                    corner_radius=6,
                                                    fg_color=("white", "gray38"))
        self.labels_frame.grid(row=0, column=0, columnspan=3, pady=10, padx=20, sticky="nsew")
        self.labels_frame.grid_rowconfigure(0, weight=1)
        self.labels_frame.grid_columnconfigure((0,1,2), weight=1)

        # Create labels
        self.label_1 = customtkinter.CTkLabel(master=self.labels_frame,
                                                text="Descripcion: " + values[0])
        self.label_1.grid(row=0, column=0, columnspan=1, rowspan=1,  pady=0, padx=10, sticky="we")

        self.label_2 = customtkinter.CTkLabel(master=self.labels_frame,
                                                text="Precio: " + values[1])
        self.label_2.grid(row=0, column=1, columnspan=1, rowspan=1,  pady=0, padx=10, sticky="we")  

        self.label_3 = customtkinter.CTkLabel(master=self.labels_frame,
                                                text="Drogueria: " + values[2])
        self.label_3.grid(row=0, column=2, columnspan=1, rowspan=1,  pady=0, padx=10, sticky="we")

        self.farma_1 = customtkinter.CTkLabel(master=self.new_window,
                                                text="Unidades " + self.farmacias_activas_abrev[0] + ": ")
        self.farma_1.grid(row=1, column=0, columnspan=1, rowspan=1,  pady=5, padx=10, sticky="we")

        self.farma_2 = customtkinter.CTkLabel(master=self.new_window,
                                                text="Unidades " + self.farmacias_activas_abrev[1] + ": ")
        self.farma_2.grid(row=1, column=1, columnspan=1, rowspan=1,  pady=5, padx=10, sticky="we")

        self.farma_3 = customtkinter.CTkLabel(master=self.new_window,
                                                text="Unidades " + self.farmacias_activas_abrev[2] + ": ")
        self.farma_3.grid(row=1, column=2, columnspan=1, rowspan=1,  pady=5, padx=10, sticky="we")

        # Create entries
        self.entry_1 = customtkinter.CTkEntry(master=self.new_window)
        self.entry_1.grid(row=2, column=0, columnspan=1, rowspan=1,  pady=5, padx=10, sticky="we")

        self.entry_2 = customtkinter.CTkEntry(master=self.new_window)
        self.entry_2.grid(row=2, column=1, columnspan=1, rowspan=1,  pady=5, padx=10, sticky="we")

        self.entry_3 = customtkinter.CTkEntry(master=self.new_window)
        self.entry_3.grid(row=2, column=2, columnspan=1, rowspan=1,  pady=5, padx=10, sticky="we")

        # Buttons grid
        self.butttons_frame = customtkinter.CTkFrame(master=self.new_window)
        self.butttons_frame.grid(row=3, column=0, columnspan=3, rowspan=1,  pady=5, padx=10, sticky="we")
        self.butttons_frame.grid_rowconfigure(0, weight=1)
        self.butttons_frame.grid_columnconfigure((0,1), weight=1)

        # Create buttons
        self.button_1 = customtkinter.CTkButton(master=self.butttons_frame,
                                                text="Aceptar",
                                                border_width=2,  # <- custom border_width
                                                command="")
        self.button_1.grid(row=0, column=0, columnspan=1, rowspan=1,  pady=5, padx=10, sticky="we")

        self.button_2 = customtkinter.CTkButton(master=self.butttons_frame,
                                                text="Cancelar",
                                                border_width=2,  # <- custom border_width
                                                command="")
        self.button_2.grid(row=0, column=1, columnspan=2, rowspan=1,  pady=5, padx=10, sticky="we")

        #Entry values
        self.entry_1.insert(0, values[3])
        self.entry_2.insert(0, values[4])
        self.entry_3.insert(0, values[5])

        # Set focus on entry
        self.entry_1.focus()

        # Bind enter key to button
        self.new_window.bind("<Return>", lambda event: print("Enter pressed"))
        self.new_window.bind("<Escape>", lambda event: self.new_window.destroy())

    def config(self):
        self.config_window = customtkinter.CTkToplevel(self)
        self.config_window.title("Configuración")
        self.config_window.geometry("400x200")
        self.config_window.maxsize(400, 200)
        self.config_window.grid_rowconfigure(0, weight=1)
        self.config_window.grid_columnconfigure(0, weight=1)
        self.config_window.update_idletasks()
        x = (self.config_window.winfo_screenwidth() - self.config_window.winfo_reqwidth()) / 2
        y = (self.config_window.winfo_screenheight() - self.config_window.winfo_reqheight()) / 2
        self.config_window.geometry("+%d+%d" % (x, y))

        # Create string variable for each farmacias activas
        self.farmacias_activas_var = []
        for i in range(len(self.farmacias_activas)):
            self.farmacias_activas_var.append(customtkinter.StringVar())
            self.farmacias_activas_var[i].set(self.farmacias_activas[i])


        # Make 3 CTkOptionMenu with the farmacias activas as default
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.config_window,
                                                        values=self.farmacias_names,
                                                        variable=self.farmacias_activas_var[0],
                                                        width=100)
        self.optionmenu_1.grid(row=0, column=0, columnspan=3, pady=10, padx=20, sticky="we")

        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.config_window, 
                                                        values=self.farmacias_names,
                                                        variable=self.farmacias_activas_var[1],
                                                        width=100)
        self.optionmenu_2.grid(row=1, column=0, columnspan=3, pady=10, padx=20, sticky="we")

        self.optionmenu_3 = customtkinter.CTkOptionMenu(self.config_window,
                                                        values=self.farmacias_names,
                                                        variable=self.farmacias_activas_var[2],
                                                        width=100)
        self.optionmenu_3.grid(row=2, column=0, columnspan=3, pady=10, padx=20, sticky="we")

        self.button_6 = customtkinter.CTkButton(master=self.config_window,
                                                text="Guardar",
                                                command=self.save_config,
                                                width=150)
        self.button_6.grid(row=3, column=0, pady=10, padx=20)

        self.config_window.bind("<Escape>", lambda event: self.config_window.destroy())
             
    def save_config(self):
        # Get the values of the 3 CTkOptionMenu
        self.farmacias_activas = []
        for i in range(len(self.farmacias_activas_var)):
            self.farmacias_activas.append(self.farmacias_activas_var[i].get())
        
        if len(set(self.farmacias_activas)) != 3:
            messagebox.showerror("Error", "No pueden haber farmacias repetidas")
            return self.config_window.destroy()

        # Update farmacias.json config file
        for farmacia in self.farmacias:
            if self.farmacias[farmacia]["nombre"] in self.farmacias_activas:
                self.farmacias[farmacia]["estado"] = "Activo"
            else:
                self.farmacias[farmacia]["estado"] = "Inactivo"
        with open("farmacias.json", "w") as f:
            json.dump(self.farmacias, f)

        self.config_window.destroy()

    def actualizar_archivos(self):
        #Create a new window
        self.update_window = customtkinter.CTkToplevel(self)
        self.update_window.title("Actualizar archivos")
        self.update_window.geometry("520x300")
        self.update_window.grid_rowconfigure(0, weight=1)
        self.update_window.grid_columnconfigure(0, weight=1)

        # Set window in the center of the screen
        self.update_window.update_idletasks()
        x = (self.update_window.winfo_screenwidth() - self.update_window.winfo_reqwidth()) / 2
        y = (self.update_window.winfo_screenheight() - self.update_window.winfo_reqheight()) / 2
        self.update_window.geometry("+%d+%d" % (x, y))

        # Create a frame
        self.update_frame = customtkinter.CTkFrame(self.update_window)
        self.update_frame.grid(row=0, column=0, columnspan=3, rowspan=3, pady=10, padx=10, sticky="nswe")
        self.update_frame.grid_rowconfigure((0,1,2,3,4), weight=1)
        self.update_frame.grid_columnconfigure((0,1), weight=1)

        self.update_label_1 = customtkinter.CTkLabel(self.update_frame, text="Ultima actualización: ")
        self.update_label_1.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="we")

        # Create a label
        self.update_label_2 = customtkinter.CTkLabel(self.update_frame,
                                                        text="Archivos seleccionados:",
                                                        text_font=("Roboto Medium", -16))
        self.update_label_2.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="nwe")

        # Create a listbox
        self.update_listbox = customtkinter.CTkTextbox(self.update_frame,
                                                        width=50,
                                                        height=100)
        self.update_listbox.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="nswe")
        # Update listbox
        self.update_file_list()

        # Create a button
        self.update_button_2 = customtkinter.CTkButton(self.update_frame,
                                                        text="Actualizar",
                                                        command=lambda: [self.save_last_update(),self.update_window.destroy()])
        self.update_button_2.grid(row=4, column=0, columnspan=1, pady=10, padx=10, sticky="we")

        # Create a button
        self.update_button_3 = customtkinter.CTkButton(self.update_frame,
                                                        text="Cancelar",
                                                        command=self.update_window.destroy)
        self.update_button_3.grid(row=4, column=1, columnspan=1, pady=10, padx=10, sticky="we")

        self.update_window.bind("<Escape>", lambda event: self.update_window.destroy())

    def update_file_list(self):
        # Get the files
        self.files = os.listdir("Archivos")
        self.files = [file for file in self.files if file.endswith(".xlsx") or file.endswith(".xls")]
        # Update the listbox
        for file in self.files:
            # Add the file name to the listbox
            self.update_listbox.insert("end", "•" + file + "\n")
        self.update_listbox.configure(state="disabled")
        # Focus on update window
        self.update_window.focus()
    
    def save_last_update(self):
        # Save the last update date in temp/config.json
        with open("temp/config.json", "r") as f:
            config = json.load(f)
        # Update the last update date
        config["last_update"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open("temp/config.json", "w") as f:
            json.dump(config, f)
        # Update the label
        self.update_label_1.configure(text="Ultima actualización: " + config["last_update"])

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()