from tkinter import *
from Multimetro import Multimeter
from Generador_senal import Gen_senal
from Aplicacion import Application
from Configuracion_widgets import *



class Main_window:
    def __init__(self,Main) -> None:
        Main.title('VENTANA PRINCIPAL')
        Main.geometry('500x500')
        Main.resizable(False,False)
        Frame1 = Frame(Main, bg='#ADD8E6')
        Frame1.pack(fill=BOTH, expand=True)

        # Buttons 
        Signal_Generator_button = Button(Frame1, text='Generador de señal', command=Gen_senal, width=25, height=2)
        config_button(Signal_Generator_button, size=20)
        Signal_Generator_button.grid(row=0, column=0, padx=(70,0), pady=40)

        Multimeter_button = Button(Frame1, text='Multímetro', command=Multimeter, width=25, height=2)
        config_button(Multimeter_button, size=20)
        Multimeter_button.grid(row=1, column=0, padx=(70,0), pady=40)

        App_button = Button(Frame1, text='Aplicación', command=Application, width=25, height=2)
        config_button(App_button, size=20)
        App_button.grid(row=2, column=0, padx=(70,0), pady=40)




window = Tk()
main_window = Main_window(window)
window.mainloop()