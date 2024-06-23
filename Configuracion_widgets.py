from tkinter import *


colour1 = '#5F9EA0' # Azul tono oscuro
colour2 = '#7FB3D5' # Azul tono claro
colour3 = '#FFFFFF' # Color blanco
colour4 = 'black'
type_hand = 'hand1' # Tipo de mano cunado pasa por encima de un Widget
type_font = 'Calibri' # Tipografía del texto
colour_background_general = '#ADD8E6' # Este color es el mismo color que el del fondo de los Frames
colour_background_boxtext_disabled = 'gray86'


def config_button(button, size):
    def on_enter(event):
            button.config(
                background=colour1,
            )

    def on_leave(event):
            button.config(
                background=colour2,

            )
            
    button.bind('<Enter>', on_enter)
    button.bind('<Leave>', on_leave)

    button.config(
            font = (type_font,size,'bold'),
            background   = colour2,
            foreground   = colour3,
            cursor = type_hand,
            bd = 1
            )



def config_OptionMenu(Option_Menu, size):

    Option_Menu.config(
        font = (type_font,size,'bold'),
        background   = colour2,
        foreground   = colour3,
        activeforeground = colour3, # Color del texto cuando el botón está activo
        activebackground = colour1, # Color de fondo cuando el botón está activo
        cursor           = type_hand,
        bd = 1,
        highlightbackground=colour_background_general,
        )


    Option_Menu['menu'].config(
        font = (type_font,size,'bold'),
        background   = colour2,
        foreground   = colour3,
        cursor = type_hand,
        activebackground = colour1,
        activeforeground = colour3 
        )




def config_Checkbutton(Checkbutton, size):
        Checkbutton.config(
            font = (type_font,size,'bold'),
            background   = colour_background_general,
            foreground   = colour4,
            cursor           = type_hand,
            bd = 0,
            selectcolor = 'white'     
            )  



def config_BoxText(BoxText, size):
      BoxText.config(
        font = (type_font, size, 'bold'),
        background = colour3,
        foreground=  colour4,
        disabledbackground = colour_background_boxtext_disabled,
        disabledforeground = colour3,
        cursor = type_hand
        )


def config_Label(Label,size):
      Label.config(
         font = (type_font, size, 'bold'), 
         foreground=  colour4, 
         background = colour_background_general
        )