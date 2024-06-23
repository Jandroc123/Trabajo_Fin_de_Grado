from tkinter import *
from tkinter import messagebox
import pyvisa
from Configuracion_widgets import *




class Gen_senal:

    def __init__(self) -> None:
        self.Resources_window = Toplevel()
        self.Resources_window.title('Selección del Instrumento')
        self.Resources_window.geometry('500x500')
        self.Resources_window.resizable(False,False)
        Resources_Frame = Frame(self.Resources_window, bd=1, relief=FLAT, bg='#ADD8E6')
        Resources_Frame.pack(fill=BOTH, expand=True)

    # Buttons
        # Menu desplegable para la elección de la dirección del Instrumento
        
        self.rm = pyvisa.ResourceManager()
        resources = self.rm.list_resources()

        self.var_OptionMenu_resources =StringVar()
        self.var_OptionMenu_resources.set(resources[0])#visualizar cajetin opcion 1 sin desplegarlo
        OptionMenu_resources = OptionMenu(Resources_Frame, self.var_OptionMenu_resources, *resources)#para desplegar las distintas opciones
        OptionMenu_resources.pack(side=TOP, pady=(100,0))
        OptionMenu_resources.config(width=20, height=2)
        config_OptionMenu(OptionMenu_resources, size=20)
        
        # Conexion
        Connection_button =Button(Resources_Frame, text='Conexión', command=self.Connection, width=20, height=2)
        config_button(Connection_button, size=20)
        Connection_button.pack(side=BOTTOM, pady=(100,100))
    

    def Connection(self):
        # Con esta función nos encargamos de que se realice la conexión con el instrumento que hemos seleccionado, abriendo la conexión usando la librería pyvisa
        # Una vez hemos hecho la conexión, destruimos la ventana 'Resources' donde solamente hemos elegido la dirección del propio instrumento que queremos para
        # así establacer la conexión
        
        
        self.Selected_resource = self.var_OptionMenu_resources.get()
        
    # Abrir conexion
        try:
            # Abrimos la conexión con el dispositivo
            self.instrument = self.rm.open_resource(self.Selected_resource)

            # Comprobamos que el recurso elegido, a través del comando *IDN que es para identifica el instrumento, coincide con el nombre del dispositivo que nos queremos conectar
            device_name = self.instrument.query('*IDN?') 

            if '33210A' in device_name: # El nombre del instrumento es '33210A'
                messagebox.showinfo('INSTRUMENTO CONECTADO',device_name)

                self.Resources_window.destroy() # Cerramos la ventana de la conexión
                
                self.Signal_generator_window()
            
            else: # En el caso de que la dirección elegida no se el dispositivo con el que nos queremos conectar
                messagebox.showwarning('WARNING','La dirección elegida no corresponde con el dispositivo seleccionado')


        except pyvisa.VisaIOError as Error:
                messagebox.showerror('ERROR','Error al conectar con el instrumento:\n'+ str(Error))
        

    #----------------------------------------------------------------------
    #----------------------------------------------------------------------
    #----------------------------------------------------------------------

    def Signal_generator_window(self):
    # Mensaje sobre informacion de la direccion del Generador de señal
        print(self.Selected_resource)


    # Creacion de diccionario para usarlo a la hora de enviar comandos SCPI y actualizar los valores 
        self.dic = {
            # Parametros generales
            'Frequency' : 'FREQ',
            'Amplitude' : 'VOLT',
            'Offset'    : 'VOLT:OFFS',
            'Impedance' : 'OUTP:LOAD',
            
            # Parametros específicos
            'Duty Cycle' : 'DCYC',
            'Symmetry'   : 'SYMM',
            'Edge Time'  : 'TRAN',

            # Tipos de funciones
            'Sine'       : 'SIN',
            'Square'     : 'SQU',
            'Ramp'       : 'RAMP',
            'Pulse'      : 'PULS',
            'Noise'      : 'NOIS',
        }

        # Diccionario con los parámetros y sus límites
        self.wave_parameters = {
            'Sine': {'Frequency': (1E-3, 10E6),'Amplitude': (0,20), 'Offset': (-10,10), 'Impedance': (0,10E3)},
            'Square': {'Frequency': (1E-3, 10E6),'Amplitude': (0,20), 'Offset': (-10,10), 'Impedance': (0,10E3), 'Duty Cycle': (20,80)},
            'Ramp': {'Frequency': (1E-3, 100E3),'Amplitude': (0,20), 'Offset': (-10,10), 'Impedance': (0,10E3), 'Symmetry': (0, 100)},
            'Pulse': {'Frequency': (1E-3,5E6),'Amplitude': (0,20), 'Offset': (-10,10), 'Impedance': (0,10E3), 'Duty Cycle': (0,100), 'Edge Time': (20E-9,100E-9)},
            'Noise': {'Frequency': (1E-3, 10E6),'Amplitude': (0,20), 'Offset': (-10,10), 'Impedance': (0,10E3)}
        }


    # Creacion ventana para configuracion de la onda
        self.Signal_Gen_window = Toplevel()
        self.Signal_Gen_window.title('GENERADOR DE SEÑAL')
        self.Signal_Gen_window.geometry('665x350')
        self.Signal_Gen_window.config(bg='#ADD8E6')
        self.Signal_Gen_window.resizable(False,False)

    # Panels
        # Panel para la configuracion de la onda junto con sus parámetros
        Panel_config_wave = LabelFrame(self.Signal_Gen_window, text='Configuración onda', font=('Calibri',10,'bold'), bd=1,relief=RAISED,bg='#ADD8E6', fg='gray25', labelanchor = 'n',  width=350, height=280)
        Panel_config_wave.grid(row=0, column=0, padx=(30,0), pady=20)
        Panel_config_wave.grid_propagate(FALSE)

        # Panel para Opciones
        Panel_Options = LabelFrame(self.Signal_Gen_window, text='Opciones', font=('Calibri',10,'bold'), bd=1,relief=RAISED, bg='#ADD8E6', fg='gray25', labelanchor = 'n',  width=250, height=280)
        Panel_Options.grid(row=0, column=1, padx=(0,10), pady=20)
        Panel_Options.grid_propagate(FALSE)


    #-------------------------------------------------------------------
    #------------------- PANEL_CONFIG_WAVE------------------------------
    #-------------------------------------------------------------------
    
    # Creación del Widget OptionMenu para la selección del TIPO DE ONDA
        Wave = ['Sine', 'Square', 'Ramp', 'Pulse', 'Noise']
        self.var_OptionMenu_wave = StringVar()
        OptionMenu_wave = OptionMenu(Panel_config_wave, self.var_OptionMenu_wave, *Wave) # El asterisco es para elegir cada una de las opciones
        self.var_OptionMenu_wave.set(Wave[0])
        self.var_OptionMenu_wave.trace_add('write',self.Update_Config_Wave_Frame) # Con esta función de aquí lo que logramos es que cada vez que cambie de valor la variable 'var_OptionMenu_wave' se llame a la función 'Update_Config_Wave_Frame'
        
        OptionMenu_wave.grid(row=0, column=0, padx=(5,0), pady = 3)
        OptionMenu_wave.config(width=7)
        config_OptionMenu(OptionMenu_wave, size = 10)

        
    # Text boxes and Chekcbuttons

        # PARAMETROS GENERALES
            # Nombres: 
            #   - Los Widgets comenzarán con el tipo de parámetro ('gen' --> General) seguido del tipo de Widget: 'gen_Checkbutton'
            #   - Las variables de cada Widget comenzará con 'var' indicando que es una variable, seguido del tipo de parámetro junto con el Widget: 'var_gen_Checbutton'

        self.general_param = ['Frequency', 'Amplitude', 'Offset','Impedance'] # Estos son parametros que van a tener todas las ondas
        self.freq_units = ['HZ', 'KHZ', 'MHZ']
        self.amplitude_units = ['VPP', 'VRMS']
        self.offset_units = ['V', 'mV']
        self.impedance_unit = ['Ω', 'KΩ']
        self.units = [self.freq_units, self.amplitude_units, self.offset_units, self.impedance_unit]


        # Creacion de Arrays correspondientes para almacenar cada uno de los Widget para cada parámetro
        self.gen_Boxtexts = []
        self.gen_Checkbuttons =[]
        self.gen_OptionMenu = []

        # Creacion de Arrays para almacenar cada una de las variables que llevan cada uno de los Widget de cada parámetro
        self.var_gen_Boxtexts = []
        self.var_gen_Checkbuttons = []
        self.var_gen_OptionMenu = []

        # Contadores: para la creación de los arrays y para la colocación de los Widget creados en diferentes filas, respectivamente
        cont_filas = 1 # Este contador comienza en 1 dado que el primer Widget que aparecerá en la pantalla es el OptionMenu para el tipo de Onda


        for cont, param in enumerate(self.general_param):
            
            # De esta manera, añadimos al array un elemento vacío el cual modificamos para añadir el Widget correspondiente
            self.gen_Checkbuttons.append('')
            self.var_gen_Checkbuttons.append('')
            self.var_gen_Checkbuttons[cont] = IntVar() #Esta variable se pondra a 1 si está seleccionada la cajetilla o 0 si no está seleccionada

            self.gen_Boxtexts.append('')
            self.var_gen_Boxtexts.append('')
            self.var_gen_Boxtexts[cont] = StringVar()
            self.var_gen_Boxtexts[cont].set('') # La cajetilla se inicializa en '' de cada parametro

            # Este Widget se usa para la selección de las unidades correspondientes de cada parámetro ya que hay varias unidades por parámetro
            self.gen_OptionMenu.append('')
            self.var_gen_OptionMenu.append('')
            self.var_gen_OptionMenu[cont] = StringVar()
            self.var_gen_OptionMenu[cont].set(self.units[cont][0]) #Sirve para inicializar la variable del Widget OptionMenu con el primer elemento de las unidades de cada parámetro: i=0 seria frecuencia y valor [0] serian los hercios -> units[cont][0]


            # Creacion de los Widget Checkbutton
            self.gen_Checkbuttons[cont] = Checkbutton(Panel_config_wave, text=param.title(),
                                onvalue=1,
                                offvalue=0,
                                variable=self.var_gen_Checkbuttons[cont],
                                command=lambda name='General': self.Check_Config_Wave_Frame(name))
            self.gen_Checkbuttons[cont].grid(row = cont_filas, column=0, sticky=W, padx=(5,0), pady = 3)
            config_Checkbutton(self.gen_Checkbuttons[cont], size = 10)



            # Creacion de los Widget Entry (BoxText)
            self.gen_Boxtexts[cont] = Entry(Panel_config_wave, 
                                          state= DISABLED, 
                                          textvariable=self.var_gen_Boxtexts[cont])
            self.gen_Boxtexts[cont].grid(row=cont_filas,column=1, pady = 3)
            config_BoxText(self.gen_Boxtexts[cont], size=10)


            # Creacion de los Widget OptionMenu para cada parámetro, conteniendo las unidades correspondientes de cada parámetro como opciones. El '*' se pone para poder elegir
            # cada uno de los elementos del array correspondiente que le hemos añadido. Así, con units[0] estaríamos haciendo referencia a las unidades del parámetro 'Frecuenqucy'
            # el cual tiene un array que coontiene las unidades ['HZ','KHZ','MHZ']
            self.gen_OptionMenu[cont] = OptionMenu(Panel_config_wave,
                                                   self.var_gen_OptionMenu[cont],
                                                   *self.units[cont])
            self.gen_OptionMenu[cont].grid(row = cont_filas, column = 2, padx=(2,0), pady = 3)
            self.gen_OptionMenu[cont].config(width = 5)
            config_OptionMenu(self.gen_OptionMenu[cont], size = 10)

            # Se incremente el valor de los contadores
            cont_filas += 1
        


        # PARAMETROS ESPECIFICOS
            # Nombres: 
            #   - Los Widgets comenzarán con el tipo de parámetro ('spec' --> Specific) seguido del tipo de Widget: 'spec_Checkbuttons'
            #   - Las variables de cada Widget comenzará con 'var' indicando que es una variable, seguido del tipo de parámetro junto con el Widget: 'var_spec_Checbuttons'

        self.specific_param = ['Duty Cycle', 'Symmetry', 'Edge Time'] # Parametros que solo aparecerán para algunos tipos de ondas

        # Creacion de los Widget Checkbutton
        self.spec_Checkbuttons = [] # Array para cada uno de los Checkbuttons que tendrá cada Parámetro Específico
        self.var_spec_Checkbuttons = [] # Array para cada una de las variables de los Checkbutton de cada Parametro Específico

        # Creacion de los Widget Entry (BoxText)
        self.spec_Boxtexts = [] # Array para cada uno de las Entries que tendrá cada Parámetro Específico
        self.var_spec_Boxtexts = [] # Array para cada una de las variables de las cajas de texto de cada Parametro Específico

        # Creación de las unidades para cada parámetro Específico junto con un array que será usado para crear etiquetas para cada tipo de unidad
        self.units_specific_param = [['%'],['%'],['nsec']] # Array para indicar el tipo de unidad e cada parametro Específico
        self.spec_OptionMenu = [] # Array usado para indicar el tipo de unidad de cada parámetro Específico mediante una etiqueta
        self.var_spec_OptionMenu = []
        

        for cont, param_spec in enumerate(self.specific_param):
            
            # Cada vez que haya una iteracion se incrementa en uno la longitud de los arrays. Asi, podemos crear y modificar ese array creado,
            # que es usado para la creacion del Checkbutton y Entries y sus respectivas variables.

            # Es necesario crear un array de variables para que asi haya una variable distinta asignada a cada elemento, sino cada vez que una 
            # se modifica una variable se modfican todas por igual

            self.spec_Checkbuttons.append('') # Array para la creacion del Widget Checkbutton. 
            self.var_spec_Checkbuttons.append('') # Array para la creacion de cada una de las variables correspondientes a los Widget Checkbutton
            self.var_spec_Checkbuttons[cont] = IntVar()

            self.spec_Boxtexts.append('') # Array para la creacion del Widget Entry
            self.var_spec_Boxtexts.append('') # Array para la creacion de cada una de las variables correspondientes a los Widget Entry
            self.var_spec_Boxtexts[cont] = StringVar()
            self.var_spec_Boxtexts[cont].set('')

            self.spec_OptionMenu.append('')
            self.var_spec_OptionMenu.append('')
            self.var_spec_OptionMenu[cont] = StringVar()
            self.var_spec_OptionMenu[cont].set(self.units_specific_param[cont][0])

            self.spec_Checkbuttons[cont] = Checkbutton(Panel_config_wave,
                                    text=param_spec.title(),
                                    onvalue=1,
                                    offvalue=0,
                                    variable=self.var_spec_Checkbuttons[cont],
                                    command=lambda name='Specific': self.Check_Config_Wave_Frame(name))
            config_Checkbutton(self.spec_Checkbuttons[cont], size=10)
            

            self.spec_Boxtexts[cont] = Entry(Panel_config_wave,
                                            state=DISABLED,
                                            textvariable=self.var_spec_Boxtexts[cont])
            config_BoxText(self.spec_Boxtexts[cont],size=10)

            
            self.spec_OptionMenu[cont] = OptionMenu(Panel_config_wave,
                                                    self.var_spec_OptionMenu[cont],
                                                    *self.units_specific_param[cont])
            self.spec_OptionMenu[cont].config(width = 5)
            config_OptionMenu(self.spec_OptionMenu[cont], size=10)

            

        # Se hace la llamada para que se actualice al principio y aparezcan los widgets correspondientes segun el tipo de onda
        self.Update_Config_Wave_Frame() 



    #-------------------------------------------------------------------
    #------------------- PANEL_OPTIONS-------------------------------
    #-------------------------------------------------------------------
    # Buttons
        self.Apply_config_onda = Button(Panel_Options, text='Aplicar Config. Onda', command=self.Validate_config_wave, width = 18, height=2)
        config_button(self.Apply_config_onda, size = 10)
        self.Apply_config_onda.grid(row=0, column=0, padx=(55,0), pady=10)

        self.ShowInfo = Button(Panel_Options,text='Información', command=self.show_info, width = 18, height=2)
        config_button(self.ShowInfo, size = 10)
        self.ShowInfo.grid(row=1, column=0, padx=(55,0), pady=10)

        self.Current_Config_button = Button(Panel_Options, text='Config actual', command=self.Current_Config, width = 18, height=2)
        config_button(self.Current_Config_button, size = 10)
        self.Current_Config_button.grid(row=2, column=0, padx=(55,0), pady=10)

        self.Disconnect_button = Button(Panel_Options, text='Desconectar', command=self.Disconnect, width = 18, height=2)
        config_button(self.Disconnect_button, size = 10)
        self.Disconnect_button.grid(row=3, column=0, padx=(55,0), pady=10)






    def validate_parameter(self,wave_type, param, value):
        # Se obtiene el valor minimo y el maximo dentro del rango de valores establecido en el diccionario y 
        # se comparan con el valor introducido

        if param == 'Impedance' and (value == 'INF' or value == 'inf'):
            return True
        else:
            min_val, max_val = self.wave_parameters[wave_type][param]
            if min_val <= float(value) <= max_val:
                return True
            else:
                return False


    def get_exponent(self,unit):
        if 'M' in unit[0]:
            return 1E6
        elif 'K' in unit[0]:
            return 1E3
        elif 'm' in unit[0]:
            return 1E-3
        elif 'n' in unit[0]:
            return 1E-9
        else:
            return 1E0


    def Validate_config_wave(self):
        # Esta función se encarga de hacer dos bucles. Unos de ellos recorriendo cada unos los parámetros generales y otro los paráemtros específicos.
        # En cada bucle se comprueba si el Checkbutton de cada parámetro está a '1', para así tenerlo en cuenta a la hora de enviar el comando SCPI, los
        # que no los tengan los obviamos (PASS). 
        
        # Para cada uno de los Checkbutton que se encuentren a '1', almacenamos en una variable el nombre del parámetro y en otra el valor que se ha 
        # introducido en la caja de texto (Entry) cambiando las comas que haya por puntos para que así no haya problemas a la hora de enviar comandos 
        # SCPI (solo aceptan puntos). Luego, se lo hacemos pasar a la función de verificar si es un número válido y así nos devuelve un booleano. Una
        # vez se ha comprobado si es un número válido, se vuelven a verificar si entran dentro de los margenes. Y si se cumple, se envia el comando SCPI
  



        mensaje = '' # Es un String que se rellena con todos los parámetros posibles que han podido tener fallo a la hora de introducir sus valores. Se debe reiniciar cada vez como una cadena vacia
        
        # Conseguimos el tipo de onda
        Type_Wave = self.var_OptionMenu_wave.get()
        self.instrument.write(f'FUNC {self.dic[Type_Wave]}')
        print(f'FUNC {self.dic[Type_Wave]}')
        self.instrument.write('OUTP ON')

        for cont, param in enumerate(self.general_param):
            
            if self.var_gen_Checkbuttons[cont].get() == 1:
                name = self.gen_Checkbuttons[cont].cget('text')
                value = self.var_gen_Boxtexts[cont].get().replace(',','.').replace('e','E')
                units = self.var_gen_OptionMenu[cont].get()
                verdict = self.verify_numeric_value(value)

                if verdict:
                        if value == 'INF' or value == 'inf': # Se pone esta condicion para evitar convertir el dato a numerico y que de un error
                            pass
                        else:
                            expo = self.get_exponent(units)
                            value = float(value)*expo

                        verdict_2 = self.validate_parameter(Type_Wave, name, value)

                        if verdict_2:
                            if name == 'Amplitude': # Se pone esta condicion ya que las unidades para la amplitud son diferentes, cambian entre VRMS o VPP, por eso es necesario CONFIGURAR LAS unidades
                                self.instrument.write(f'{self.dic[name]}:UNIT {units}')
                                print(f'{self.dic[name]}:{units}')
                                self.instrument.write(f'{self.dic[name]} {value} {units}')
                                print(f'{self.dic[name]} {value}')

                            else:                        
                                self.instrument.write(f'{self.dic[name]} {value}')
                                print(f'{self.dic[name]} {value}')
            
                        else:
                            mensaje = mensaje + f'El valor para {name} no se encuentra en el rango\n'

                else:
                    mensaje = mensaje + f'El valor para {name} no se ha introducido correctamente\n'
            else:
                pass

        
        for cont, param, in enumerate(self.specific_param):
            
            if self.var_spec_Checkbuttons[cont].get() == 1:
                name = self.spec_Checkbuttons[cont].cget('text') 
                value = self.var_spec_Boxtexts[cont].get().replace(',','.').replace('e','E')
                units = self.var_spec_OptionMenu[cont].get()
                verdict = self.verify_numeric_value(value)
                
                if verdict:
                    expo = self.get_exponent(units)
                    value = float(value)*expo
                    verdict_2 = self.validate_parameter(Type_Wave, name, value)       

                    if verdict_2:
                            self.instrument.write(f'FUNC:{self.dic[Type_Wave]}:{self.dic[name]} {value}')
                            print(f'FUNC:{self.dic[Type_Wave]}:{self.dic[name]} {value}')
                                     
                    else:
                        mensaje = mensaje + f'El parámetro {name} está fuera de rango\n'
                else:
                    mensaje = mensaje + f'El parámetro {name} no se ha introducido correctamente\n'

        # Mostrar mensaje de Warning si se ha cometido algún error a la hora de introducir datos
        if mensaje != '':
            messagebox.showwarning('Advertencia',mensaje)
        else:
            pass
    



    def Check_Config_Wave_Frame(self,name):
            # Con esta funcion realizamos un bucle del mismo numero de parametros generales que tengamos. En él, comprobamos si los Checkbutton
            # han sido seleccionados (cuando se seleccionan su valor se vuelva a 1) y si está seleccionado cambiamos la configuración de la caja
            # de texto (Entry) para que así podamos escribir en ella. Si el valor que hay en la caja de texto es '0', se elimina dicho valor y 
            # centramos el cursor en la caja de texto. En otro caso, cuando el Checkbutton del parametro se encuentra deseleccionado (valor 0)
            # cambiamos la configuracion de la caja de texto para que no se pueda escribir en ella y ponemos el valor de la variable de la caja
            # de texto al valor '0'
        
            if name == 'General':

                for cont, param in enumerate(self.gen_Boxtexts):
                    if self.var_gen_Checkbuttons[cont].get() == 1:
                        self.gen_Boxtexts[cont].config(state=NORMAL)

                        if self.var_gen_Boxtexts[cont].get() == '':
                            self.gen_Boxtexts[cont].delete(0,END)
                    
                        self.gen_Boxtexts[cont].focus()

                    else:
                        self.gen_Boxtexts[cont].config(state=DISABLED)
                        self.var_gen_Boxtexts[cont].set('')


            elif name == 'Specific':

                for cont, param in enumerate(self.specific_param):
                    if self.var_spec_Checkbuttons[cont].get() == 1:
                        self.spec_Boxtexts[cont].config(state = NORMAL)

                        if self.var_spec_Boxtexts[cont].get() == '':
                            self.spec_Boxtexts[cont].delete(0,END)

                        self.spec_Boxtexts[cont].focus()

                    else:
                        self.spec_Boxtexts[cont].config(state=DISABLED)
                        self.var_spec_Boxtexts[cont].set('')





    def verify_numeric_value(self,value):
    # Con esta función nos encargamos de:
    #   1º Comprobar  que no haya '_' ya que la conversión a float acepta este caracter, comprobar que el valor sea INF y hacer la conversión a float
    #   2º Devolver Fasle si contiene '_', devolver True si es INF o intentar hacer la conversion a float, que si da fallo la conversion se comtempla con ValueError, para devolver False

        try:
            if ('_' in value): # Flaot acepta un barra baja
                return False
            elif value == 'INF' or value == 'inf':
                return True
            else:
                float(value)
                return True
            
        except ValueError: # Si hay alguna error en la conversión mediante float salta este error
            # Si ocurre un ValueError, significa que la cadena no representa un número decimal válido
            return False


    def Update_Config_Wave_Frame(self,*args):
        
        # Primero, comprobamos que tipo de funcion se ha elegido. Si es una de las que tiene parametros Específicoes se actualizan los parametros
        # visibles. Segundo, se hace un bucle con todas las iteracions posibles segun el numero de parametros Específicoes donde para cada 
        # Checkbutton y Entry asignadado a cada parametros Específico se le asigna la funcion grid_forget, para que asi una vez se elija una funcion
        # distinta se actualicen tambien los parametros, es decir, si aparecen o desaparecen segun la funcion elegida.
        # Por ultimo, se comprueba el tipo de funcion elegida y se dibujan en pantalla los parametros correspondientes

        # '*args' en Python es un parámetro Específico que se utiliza para pasar un número variable de argumentos a una función. 
        # La palabra clave args es solo una convención, y el asterisco (*) indica que cualquier cantidad de argumentos 
        # posicionales pueden ser pasados a la función, y estos serán recopilados en una tupla llamada args

        # Aquí, *args se utiliza simplemente para indicar que la función Update_Config_Wave_Frame() puede recibir cualquier número 
        # de argumentos, pero en realidad no estamos usando esos argumentos dentro de la función.

        # Almacenamos en una variable el tipo de onda seleccionada
        Type_Wave = self.var_OptionMenu_wave.get()
        

        # Este bucle es realizado para resetear todos los widget una vez se elige un parametro  para que asi no se queden en pantalla los que no corresponden con el tipo de onda
        for cont, param in enumerate(self.specific_param):
            self.spec_Checkbuttons[cont].grid_forget()
            self.spec_Boxtexts[cont].grid_forget()
            self.spec_OptionMenu[cont].grid_forget()

            # Esta sentencia sirve para que si en el caso de que cambiemos de tipo de onda sin haber deseleccionado la opcion del parametro Específico, una vez se vuelva a elegir el mismo tipo de onda no siga seleccionada
            self.var_spec_Checkbuttons[cont].set(0)  
            
            # Para que cuando se cambie de onda sin haber quitado el valor que habia se ponga a '' y se desactive el BoxText
            self.var_spec_Boxtexts[cont].set('') 
            self.spec_Boxtexts[cont].config(state=DISABLED)


        for cont, param in enumerate(self.general_param):
            self.var_gen_Checkbuttons[cont].set(0)
            self.var_gen_Boxtexts[cont].set('')
            self.gen_Boxtexts[cont].config(state=DISABLED)



        if Type_Wave == 'Square':
            self.spec_Checkbuttons[0].grid(row=5, column=0, sticky = W, padx = (5,0), pady = 3)
            self.spec_Boxtexts[0].grid(row=5,column=1, pady = 3)
            self.spec_OptionMenu[0].grid(row=5,column=2,sticky = S, padx = (0,5), pady = 3)

            
        
        elif Type_Wave == 'Ramp':
            self.spec_Checkbuttons[1].grid(row=5, column=0, sticky = W, padx = (5,0), pady = 3)
            self.spec_Boxtexts[1].grid(row=5,column=1, pady = 3)
            self.spec_OptionMenu[1].grid(row=5,column=2,sticky = S, padx = (2,5), pady = 3)

            
        
        elif Type_Wave == 'Pulse':
            self.spec_Checkbuttons[0].grid(row=5, column=0, sticky = W, padx = (5,0), pady = 3)
            self.spec_Boxtexts[0].grid(row=5,column=1, pady = 3)
            self.spec_OptionMenu[0].grid(row=5,column=2,sticky = S,padx = (0,5), pady = 3)

            self.spec_Checkbuttons[2].grid(row=6, column=0, sticky = W, padx = (5,0), pady = 3)
            self.spec_Boxtexts[2].grid(row=6,column=1, pady = 3)
            self.spec_OptionMenu[2].grid(row=6,column=2,sticky = S, padx = (2,5), pady = 3)


        else:
            pass
        


    def Disconnect(self):
        # Esta función se encargará de hacer la desconexión con el dispositivo y cerrar la salida del generador del señal
        self.instrument.write('OUTP OFF')
        self.instrument.close()
        self.Signal_Gen_window.destroy()   


    def Current_Config(self):
        wave = self.instrument.query('FUNC?')
        units = self.instrument.query('VOLT:UNIT?')
        amplitude = self.instrument.query('VOLT?')
        offset = self.instrument.query('VOLT:OFFS?')
        frequency = self.instrument.query('FREQ?')
        impedance = self.instrument.query('OUTP:LOAD?')
        
        message = f'Onda actual : {wave}\nAmplitud : {amplitude} {units}\nOffset : {offset}\nFrecuencia : {frequency}\nImpedancia : {impedance} '

        messagebox.showinfo('CONFIGURACIÓN ACTUAL', message)
            


    def show_info(self):
        # Funcion para mostrar informacion sobre como introducir los valores para la impedancia
        message = ( 
                    "-Impedancia -> [1,10K] Ω \n"
                    "-Duty Cycle de Onda Cuadrada - > [20,80]%\n"
                    "-Simetría y Duty Cycle -> [1,100]%\n"
                    "-Edge Time -> [20,100] ns\n"
                    "-Datos con formato -> 3E+05, 45.6\n"
                    "-Sin, Square Max Freq -> 10MHz\n"
                    "-Pulse Max Freq -> 5MHz\n"
                    "-Ramp Max Freq -> 100KHz\n"
                    "-Amplitude -> [0,20]\n"
                    "-Offset -> [-10,10] V\n"
                  )
        messagebox.showinfo('INFORMACION',message)





