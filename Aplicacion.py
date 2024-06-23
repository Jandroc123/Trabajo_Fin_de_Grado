from tkinter import *
from tkinter import messagebox
import pyvisa
from Configuracion_widgets import *
import matplotlib.pyplot as plt


class Application:
    def __init__(self) -> None:
        self.Resources_window = Toplevel()
        self.Resources_window.title('Selección de los Instrumentos')
        self.Resources_window.geometry('500x500')
        Resources_Frame = Frame(self.Resources_window, bd=1, relief=FLAT, bg='#ADD8E6')
        Resources_Frame.pack(fill=BOTH, expand=True)

    # Buttons
        # Menu desplegable para la elección de la dirección del Instrumento
        
        self.rm = pyvisa.ResourceManager()
        resources = self.rm.list_resources()
        

        # resources = ['1345435','2454543','3435435']

        # Se hace un bucle de 2 iteraciones para crear 2 OptionMenu en los cuales se eligirá el Multímetro y el Generador de señal
        self.Resources_OptionMenu = []
        self.var_Resources_OptionMenu = []

        self.Resources_Labels = []
        self.Labels = ['Generador de señal', 'Multímetro']

        for cont in range(2):
            self.Resources_OptionMenu.append('')
            self.var_Resources_OptionMenu.append('')
            self.var_Resources_OptionMenu[cont] = StringVar()
            self.var_Resources_OptionMenu[cont].set(resources[0])

            self.Resources_Labels.append('')
            self.Resources_Labels[cont] = Label(Resources_Frame, text=self.Labels[cont])
            config_Label(self.Resources_Labels[cont], size=15)

            self.Resources_OptionMenu[cont] = OptionMenu(Resources_Frame,
                                                         self.var_Resources_OptionMenu[cont],
                                                         *resources)
            self.Resources_OptionMenu[cont].config(width=20, height=2)
            config_OptionMenu(self.Resources_OptionMenu[cont], size=15)
        
        # Colocación de los Widgets
        
        # Generador de señal
        self.Resources_Labels[0].grid(row=0, column=0, padx=(130,0), pady=(50,1)) 
        self.Resources_OptionMenu[0].grid(row=1, column=0, padx=(130,0), pady=(0,50)) 

        #Multímetro
        self.Resources_Labels[1].grid(row=2, column=0, padx=(130,0), pady=(0,1)) 
        self.Resources_OptionMenu[1].grid(row=3, column=0, padx=(130,0), pady=(0,50))


        # Conexion
        Connection_button =Button(Resources_Frame, text='Conexión', command=self.Connection, width=20, height=2)
        config_button(Connection_button, size=15)
        Connection_button.grid(row=4, column=0, padx=(130,0), pady=(30,50))

    
    def Connection(self):

        self.Selected_resource_Signal_Gen = self.var_Resources_OptionMenu[0].get() # Primera posición del array correponde con el Generador de señal
        self.Selected_resource_Multimeter = self.var_Resources_OptionMenu[1].get() # Segunda posición del array corresponde con el Multímetro

        try:
            # Abrimos la conexión con los dos instrumentos
            self.Signal_Generator = self.rm.open_resource(self.Selected_resource_Signal_Gen)
            self.Multimeter = self.rm.open_resource(self.Selected_resource_Multimeter)

            # Comprobamos que el recurso elegido, a través del comando *IDN que es para identifica el instrumento, coincide con el nombre del dispositivo que nos queremos conectar
            self.Signal_Generator_name = self.Signal_Generator.query('*IDN?')
            self.Multimeter_name = self.Multimeter.query('*IDN?')

            if ('33210A' in self.Signal_Generator_name) and ('34461A' in self.Multimeter_name): 
                messagebox.showinfo('INSTRUMENTOS CONECTADOS',f'{self.Signal_Generator_name}\n{self.Multimeter_name}')

                self.Resources_window.destroy() # Cerramos la ventana de la conexión
                
                self.Application_window() # Una vez se ha verificado que el instrumetno es el correcto, se llama a la funcion Multimeter_window
            
            else: # En el caso de que la dirección elegida no se el dispositivo con el que nos queremos conectar
                if ('33210A' not in self.Signal_Generator_name) and ('34461A' not in self.Multimeter_name): # En el caso de que ninguna direccion coincida con la que queremos
                    messagebox.showwarning('WARNING','La direcciones elegidas no corresponden')

                elif '34461A' not in self.Multimeter_name: # En caso de que la direccion del multímetro no sea la correcta
                    messagebox.showwarning('WARNING','La dirección elegida para el Multímetro no corresponde\n')

                else: # En el caso de que la dirección cdel generador de señal no sea la adecuada
                    messagebox.showwarning('WARNING','La dirección elegida para el Generador de señal no corresponde\n')


        except pyvisa.VisaIOError as Error:
                messagebox.showerror('ERROR','Error al conectar con el instrumento:\n'+ str(Error))
    


    def Application_window(self):
        self.App_window = Toplevel()
        self.App_window.title('APLICACIÓN')
        self.App_window.geometry('900x500')
        self.App_window.config(bg='#ADD8E6')
        self.App_window.resizable(False,False)


    # Creacion de diccionario para usarlo a la hora de enviar comandos SCPI y actualizar los valores 
        self.dic = {
            # Parametros generales
            'Frequency' : 'FREQ',
            'Amplitude' : 'VOLT',
    
            # Tipos de funciones
            'Sine'       : 'SIN',
            'Square'     : 'SQU',
            'Ramp'       : 'RAMP',
            'Pulse'      : 'PULS',
            'Noise'      : 'NOIS',
        }

    # Arrays para almacenar las frecuencias obtenidas y las amplitudes en las iteraciones para hallar la frecuencia de corte
        self.Frequencies = []
        self.Amplitudes = []

    # Panels
        # Panel para la configuracion de la onda junto con sus parámetros
        Panel_Config_App = LabelFrame(self.App_window, text='Configuración onda', font=('Calibri',10,'bold'), bd=1,relief=RAISED,bg='#ADD8E6', fg='gray25', labelanchor = 'n',  width=305, height=400)
        Panel_Config_App.grid(row=0, column=0, padx=(15,0), pady=20)
        Panel_Config_App.grid_propagate(FALSE)

        # Panel para mostrar los resultados obtenidos de cada iteración y la frecuencia de corte final
        Panel_Show_Info = LabelFrame(self.App_window, text='Resultados', font=('Calibri',10,'bold'), bd=1,relief=RAISED, bg='#ADD8E6', fg='gray25', labelanchor = 'n',  width=310, height=400)
        Panel_Show_Info.grid(row=0, column=1, pady=20)
        Panel_Show_Info.grid_propagate(FALSE)

        # Panel para Opciones
        Panel_Options = LabelFrame(self.App_window, text='Opciones', font=('Calibri',10,'bold'), bd=1,relief=RAISED, bg='#ADD8E6', fg='gray25', labelanchor = 'n',  width=250, height=400)
        Panel_Options.grid(row=0, column=2, padx=(0,15), pady=20)
        Panel_Options.grid_propagate(FALSE)

    
    #-------------------------------------------------------------------
    #------------------- Panel_Config_App------------------------------
    #-------------------------------------------------------------------
    
    # Creación del Widget OptionMenu para la selección del TIPO DE ONDA
        Wave = ['Sine', 'Square', 'Ramp', 'Pulse']
        self.var_OptionMenu_wave = StringVar()
        OptionMenu_wave = OptionMenu(Panel_Config_App, self.var_OptionMenu_wave, *Wave) # El asterisco es para elegir cada una de las opciones
        self.var_OptionMenu_wave.set(Wave[0])
        OptionMenu_wave.grid(row=0, column=0, padx=(5,0), pady = 3)
        OptionMenu_wave.config(width=7)
        config_OptionMenu(OptionMenu_wave, size = 10)

        # Se declara un array con todos los parámetros que se pueden modificar junto con los arrays correspondientes de los widgets para los parámetros
        self.Parameters = ['Amplitude', 'Frequency', 'Initial Step', 'Second Step']
        self.Parameters_Checkbutton = [] # Para poder elegir seleccionar los parámetros
        self.var_Parameters_Checkbutton = []
        self.Parameters_BoxText = [] # Para introducir el valor de los parámetros
        self.var_Parameters_BoxText = []

        self.Units = ['Vrms', 'Hz', 'Hz', 'Hz'] # Las unidades para cada parámetro
        self.Units_Labels = [] # Un array para crear cada etiqueta de cada parametro para colocar las unidades

        for cont, param in enumerate(self.Parameters):
            
            # PARA LA COLOCACION DE LAS FILAS SE AÑADE +1 YA QUE LA ELECCION DEL TIPO DE ONDA SE ENCUENTRA EN LA FILA NUMERO 0
            
            self.Parameters_Checkbutton.append('')
            self.var_Parameters_Checkbutton.append('')
            self.var_Parameters_Checkbutton[cont] = IntVar()

            self.Parameters_BoxText.append('')
            self.var_Parameters_BoxText.append('')
            self.var_Parameters_BoxText[cont] = StringVar()
            self.var_Parameters_BoxText[cont].set('')

            self.Units_Labels.append('')

            # Creacion para los Checkbuttons
            self.Parameters_Checkbutton[cont] = Checkbutton(Panel_Config_App,
                                                            text = param.title(),
                                                            onvalue=1,
                                                            offvalue=0,
                                                            variable=self.var_Parameters_Checkbutton[cont],
                                                            command=self.Check_Config_App_Frame)
            self.Parameters_Checkbutton[cont].grid(row=cont+1, column=0, padx=(10,0), pady=(20,20))
            config_Checkbutton(self.Parameters_Checkbutton[cont],size=10)


            # Creacion para las cajas de texto
            self.Parameters_BoxText[cont] = Entry(Panel_Config_App,
                                                  state=DISABLED,
                                                  textvariable=self.var_Parameters_BoxText[cont])
            self.Parameters_BoxText[cont].grid(row=cont+1, column=1, padx=(10,0), pady=(20,20))
            config_BoxText(self.Parameters_BoxText[cont],size=10)


            # Creacion para las eitquetas de de cada parametro
            self.Units_Labels[cont] = Label(Panel_Config_App, text = self.Units[cont])
            self.Units_Labels[cont].grid(row=cont+1, column=2, padx=(10,0), pady=(20,20))
            config_Label(self.Units_Labels[cont], size=10)




    #-------------------------------------------------------------------
    #------------------- PANEL_SHOW_INFO-------------------------------
    #-------------------------------------------------------------------

            # Creacion del array con los diferentes tipos de medida que se calculan y sus widgets correspondientes 
            self.Measures = ['Sweep Amplitude', 'Sweep Frequency', 'Cutoff Freq']

            self.Measures_Labels = []
            self.Measures_Boxtexts = []
            self.var_Measures_Boxtexts = []


            # Bucle para la creacion de los widgets correspondientes para las diferentes medidas
            for cont, param in enumerate(self.Measures):
                
                # Proceso para añadir elementos al array correspondiente e inicializar las variables
                self.Measures_Labels.append('')

                self.Measures_Boxtexts.append('')
                self.var_Measures_Boxtexts.append('')
                self.var_Measures_Boxtexts[cont] = StringVar()
                self.var_Measures_Boxtexts[cont].set('')


                # Creacion de las etiquetas
                self.Measures_Labels[cont] = Label(Panel_Show_Info, text=self.Measures[cont])
                self.Measures_Labels[cont].grid(row=cont, column=0, padx=(5,10), pady=(30,30))
                config_Label(self.Measures_Labels[cont], size=10)


                # Creacion de las cajas de texto
                self.Measures_Boxtexts[cont] = Entry(Panel_Show_Info, state = NORMAL, textvariable=self.var_Measures_Boxtexts[cont])
                self.Measures_Boxtexts[cont].grid(row=cont, column=1, pady=(30,30))
                config_BoxText(self.Measures_Boxtexts[cont], size=10)


    #-------------------------------------------------------------------
    #------------------- PANEL_OPTIONS-------------------------------
    #-------------------------------------------------------------------
    # Buttons
        self.Initial_step_button = Button(Panel_Options, text='Iniciar Primer Bucle', command=self.First_loop, width = 15, height=2)
        config_button(self.Initial_step_button, size = 10)
        self.Initial_step_button.grid(row=0, column=0, padx=(65,0), pady=15)

        self.Second_step_button = Button(Panel_Options, text='Iniciar Segundo Bucle', command=self.Second_loop, width = 15, height=2)
        config_button(self.Second_step_button, size = 10)
        self.Second_step_button.grid(row=1, column=0, padx=(65,0), pady=15)

        self.ShowInfo_button = Button(Panel_Options,text='Información', command=self.show_info, width = 15, height=2)
        config_button(self.ShowInfo_button, size = 10)
        self.ShowInfo_button.grid(row=2, column=0, padx=(65,0), pady=15)

        self.Graphic_button = Button(Panel_Options,text='Graficar', command=self.Graphic, width = 15, height=2)
        config_button(self.Graphic_button, size = 10)
        self.Graphic_button.grid(row=3, column=0, padx=(65,0), pady=15)

        self.Disconnect_button = Button(Panel_Options, text='Desconectar', command=self.Disconnect, width = 15, height=2)
        config_button(self.Disconnect_button, size = 10)
        self.Disconnect_button.grid(row=4, column=0, padx=(65,0), pady=15)


    def Check_Config_App_Frame(self):

        for cont, param in enumerate(self.Parameters):
            if self.var_Parameters_Checkbutton[cont].get() == 1:
                self.Parameters_BoxText[cont].config(state=NORMAL)

                if self.var_Parameters_BoxText[cont].get() == '':
                    self.Parameters_BoxText[cont].delete(0,END)
                
                self.Parameters_BoxText[cont].focus()
            
            else:
                self.Parameters_BoxText[cont].config(state=DISABLED)
                self.var_Parameters_BoxText[cont].set('')



    def First_loop(self):

        # En primar lugar, hay que enviar varios comandos de configuracon para el multimetro, configurando el tipo de medida a voltaje de corriente alterna,
        # ajustar el filtro de corriente alterna a 3 Hz por las frecuencias pequeñas de la señal, habiliatar la salida del generador de señal, ajustar 
        # que el tipo de unidad para la amplitud esta en Vrms y ajustar una alta impedancia de salida para el generador de señal permita sacar
        # el mismo valor de la amplitud que se ha ajustado

        self.Multimeter.write('CONF:VOLT:AC')
        self.Multimeter.write('VOLT:AC:BAND 3')
        self.Signal_Generator.write('OUTP ON')
        self.Signal_Generator.write('VOLT:UNIT VRMS')
        self.Signal_Generator.write(f'OUTP:LOAD INF')

        # Se reestablecen los valores de las cajas de texto de las medidas como vacíos
        for cont,param in enumerate(self.Measures):
            self.var_Measures_Boxtexts[cont].set('')

        # Segundo, se verifica que los parametros han sido elegidos y que estos tienen un valor adecuado para realizar el primer bucle

        # Se configura el generador de señal con la onda elegida
        Type_Wave = self.dic[self.var_OptionMenu_wave.get()]
        self.Signal_Generator.write(f'FUNC {Type_Wave}')
        print(f'FUNC {Type_Wave}')
        

        # CREACION DE VARIABLES Y ARRAYS
        
        # Variable booleana que sirve para que se realice el bucle (True) si todos los paráemtros han sido configurados correctamente
        self.Loop = False

        # String para almacenar los mensajes de error
        self.Message = ''

        # Arrays para almacenar cada valor de la frecuencia y amplitud en las iteraciones 
        self.Frequencies = [] # Se iniciliza como array vacío cada vez que se llame a la función
        self.Amplitudes  = [] # Se iniciliza como array vacío cada vez que se llame a la función

        # VAaribales donde se almacena la frecuencia de corte (que sera un intervalo), la frecuencia de barrido (que se incrementa en cada iteracion con el paso seleccionado)
        # la amplitud de barrido (que cambia en cada paso con el valor obtenido de la medicion, ya que depende de la frecuencia), y los valores inicales para la amplitud 
        # la frecuencia y el paso establecido
        self.Cutoff_Freq = ''
        self.Sweep_Amplitude = ''
        self.Sweep_Freq = ''
        self.Initial_Amplitude = ''
        self.Initial_Freq = ''
        self.Step = ''


        # Se realiza un primer bucle para verificar que los parametros de: La frecuencia, la amplitud y el primer paso (Initial Step) sean válidos para realizar el primer bucle.
        # Para este bucle principal no hace falta comprobar el valor establecido para el parametro Second Step, ya que no influye en la realizacion del primer bucle.
        for cont in range(len(self.Parameters)-1): 
            
            name = self.Parameters_Checkbutton[cont].cget('text')

            if self.var_Parameters_Checkbutton[cont].get() == 1:
                value = self.var_Parameters_BoxText[cont].get()
                verdict = self.verify_numeric_value(value)

                if verdict:
                    if float(value) > 0: # Se comprueba que el valor es mayor que 0
                        if name == 'Initial Step': # Para el parametro Initial Step no hace falta enviar, por eso se pasa
                            pass
                        else:
                            self.Signal_Generator.write(f'{self.dic[name]} {value}')
                            print(f'{self.dic[name]} {value}')

                        self.Loop = True

                    else:
                        self.Message = self.Message + f'El valor introducido para {name} debe ser mayor que 0\n'
                        self.Loop = False
                else:
                    self.Message = self.Message + f'El valor introducido para {name} no es válido\n'
                    self.Loop = False

            else:
                self.Message =self.Message + f'No se ha seleccionado el parámetro {name}\n'
                self.Loop = False
        


        
        # Si todos los parámetros para el primer bucle son válidos, se inica el bucle, donde se obtienen los valores que se han introducido
        if self.Loop:

            self.Initial_Freq = self.var_Parameters_BoxText[1].get() # Corresponde con la frecuencia que se ha introducido para la señal
            self.Sweep_Freq = self.Initial_Freq # El valor para la frecuencia de barrido, que es la que se envia en cada iteracion al generador de señal, se inicializa con la frecuena de la señal
            self.Step = self.var_Parameters_BoxText[2].get() # Se almacena el valor del paso establecido para el primer bucle
            self.Initial_Amplitude = self.var_Parameters_BoxText[0].get() # Corresponde al valor de la amplitud de la señal
            self.Sweep_Amplitude = self.Initial_Amplitude # La amplitud de barrido se inicializa con el valor de la amplitud inicial

            # Los valores de la frecuencia y la amplitud inicales se introducen en el array correspondiente que sevirá para mostrar los datos en una gráfica posteriomente
            self.Amplitudes.append(float(self.Initial_Amplitude))
            self.Frequencies.append(float(self.Initial_Freq))

            # Se inicia el bucle. Mientras la amplitud obtenida por el multimetro de la señal sea mayor que el 70% del valor de la amplitud inicial se sigue iterando aumentando
            # el valor de la frecuencia por lo que el valor de la amplitud de la señal irá disminuyendo debido al filtro
            while(float(self.Sweep_Amplitude) > (float(self.Initial_Amplitude)*0.7)):
                self.Sweep_Freq = float(self.Sweep_Freq) + float(self.Step) # Se aumenta el valor de la frencuecia de barrido en el número de paso que se ha establecido
                self.Signal_Generator.write(f'FREQ {self.Sweep_Freq}') # Se envia el valor de la frecuencia de barrido al generador de señal 
                self.var_Measures_Boxtexts[1].set(str(self.Sweep_Freq)) # Se muestra el valor de la frecuencia de barrido en la caja de texto
                print(f'FREQ: {self.Sweep_Freq}')

                self.Sweep_Amplitude = float(self.Multimeter.query('READ?'))
                self.var_Measures_Boxtexts[0].set(str(self.Sweep_Amplitude))

                # Cada valor obtenido se almacenan en los arrays correspondientes
                self.Frequencies.append(self.Sweep_Freq)
                self.Amplitudes.append(self.Sweep_Amplitude)

                self.App_window.update() # Utilizado para forzar la actulizacion de la ventna y que se vean los resultados

            # Se obtienen los umbrales que establecen entre que valores esta la frecuencia de corte
            self.Cutoff_Freq_umbral_1 = self.Frequencies[len(self.Frequencies)-2] # Se obtiene el penultimo valor calculado de la frecuencia, el anterior al de la freq de corte
            self.Cutoff_Freq_umbral_2 = self.Frequencies[len(self.Frequencies)-1] #Se obtiene el ultimo valor del array, que es en el cual la amplitud ya es menor
            Cutoff_freq = f'[{self.Cutoff_Freq_umbral_1}, {self.Cutoff_Freq_umbral_2}]'
            self.var_Measures_Boxtexts[2].set(Cutoff_freq)
            print(f'Frecuencia de corte se encuentra entre : [{self.Cutoff_Freq_umbral_1},{self.Cutoff_Freq_umbral_2}]')


        else:
            self.Message = self.Message + f'NO SE HA REALIZADO EL CÁLCULO DE LA FRECUENCIA DE CORTE\n' # Mensaje que indica que no se ha podido realizar el bucle


        if self.Message!='':
            messagebox.showwarning('WARNING', self.Message)
        else:
            pass




    def Second_loop(self):
        # Primero comprobar que esté seleccionado el parámetro 'Second Step' y si lo está y es un valor válido, verificar que que el array de Frecuencias 
        # y amplitudes adquiridas no esté vacío. Esto quiere decir que se ha hecho primero el primer bucle para hallar la frecuencia de corte

        self.Sweep_Freq = ''
        self.Sweep_Amplitude =''
        self.Second_Step = ''

        # Se borran los valores de las cajas de texto para la amplitud y frecuencia
        self.var_Measures_Boxtexts[0].set('')
        self.var_Measures_Boxtexts[1].set('')

        if self.var_Parameters_Checkbutton[3].get() == 1:
            value = self.var_Parameters_BoxText[3].get()
            verdict = self.verify_numeric_value(value)

            if verdict:
                if float(value)>0:
                    self.Second_Step = value

                    if (len(self.Frequencies)>1): # Solo basta con comprobar un array. Si la longitud es mayor que 1 significa que se ha podido realizar 
                        
                        # Estos valores son clave para iniciar el segundo bucle, ya que a partir de estos valores es de donde se incrementa la frecuencia 
                        # y la amplitud de barrido
                        self.Sweep_Freq = self.Frequencies[len(self.Frequencies)-2] # Cogemos el valor de antes de la frecuencia de corte
                        self.Sweep_Amplitude = self.Amplitudes[len(self.Amplitudes)-2] # Cogemos el valor de la amplitud antes de la frecuencia de corte

                        # Es necesario borrar los últimos valores de los arrays ya que estos son de la antigua frecuencia de corte, no los necesitamos
                        self.Frequencies.pop() # Se borran las últimas posiciones de los arrays ya que estos corresponden con la frecuencia de corte de antes
                        self.Amplitudes.pop() # Se borra el ultimo valor ya que es el de la frecuena de corte pasada, no nos interesa tenerlo porque vamos a calcular otra


                        while(float(self.Sweep_Amplitude) > (float(self.Initial_Amplitude)*0.7)):
                            self.Sweep_Freq = float(self.Sweep_Freq) + float(self.Second_Step)
                            self.Signal_Generator.write('FREQ ' + str(self.Sweep_Freq))
                            self.var_Measures_Boxtexts[1].set(str(self.Sweep_Freq)) # Se muestra el valor de la frecuencia de barrido en la caja de texto

                            self.Sweep_Amplitude = float(self.Multimeter.query('READ?'))
                            self.var_Measures_Boxtexts[0].set(str(self.Sweep_Amplitude))

                            # Se añaden los nuevos valores obtenidos de las frecuencias y amplitudes a los arrays
                            self.Frequencies.append(self.Sweep_Freq)
                            self.Amplitudes.append(self.Sweep_Amplitude)

                            self.App_window.update() # Utilizado para forzar la actulizacion de la ventna y que se vean los resultados

                        self.Cutoff_Freq_umbral_1 = self.Frequencies[len(self.Frequencies)-2]
                        self.Cutoff_Freq_umbral_2 = self.Frequencies[len(self.Frequencies)-1]
                        Cutoff_freq = f'[{self.Cutoff_Freq_umbral_1}, {self.Cutoff_Freq_umbral_2}]'
                        self.var_Measures_Boxtexts[2].set(Cutoff_freq)
                        print(f'Frecuencia de corte se encuentra entre : [{self.Cutoff_Freq_umbral_1},{self.Cutoff_Freq_umbral_2}]')

                    else:
                        messagebox.showwarning('WARNING', 'Se debe realizar el primer bucle')
                else:
                    messagebox.showwarning('WARNING', 'El valor para el segundo paso debe ser mayor que 0')
            else:
                messagebox.showwarning('WARNING', 'El valor introducido para "Second Step" no es válido')
        else:
            messagebox.showwarning('WARNING', 'No se ha seleccionado "Second Step"')




    def Graphic(self):

        plt.figure(figsize=(10, 6))
        plt.plot(self.Frequencies, self.Amplitudes, color='red', label='Línea')
        plt.scatter(self.Frequencies, self.Amplitudes, color='blue', label='Puntos')

        # Añadir etiquetas y título
        plt.xlabel('Frecuencia')
        plt.ylabel('Amplitud')
        plt.title('Frecuencia de corte')
        plt.legend()

        # Mostrar la gráfica
        plt.show()



    def verify_numeric_value(self,value):
        try:
            if ('_' in value):
                return False
            else:
                float(value)
                return True
            
        except ValueError:
            return False




    def Disconnect(self):
        # Esta función se encargará de hacer la desconexión con el dispositivo y cerrar la salida del generador del señal
        self.Signal_Generator.write('OUTP OFF')
        self.Signal_Generator.close()
        self.Multimeter.close()
        self.App_window.destroy()   
        

    def show_info(self):
        # Funcion para mostrar informacion sobre como introducir los valores para la impedancia
        mensaje = ( 
                    "-Impedancia -> [1,10K] Ω o INF (Alta impedancia)\n"
                    "-Duty Cycle de Onda Cuadrada - > [20,80]%\n"
                    "-Simetría y Duty Cycle -> [1,100]%\n"
                    "-Edge Time -> [20,100] ns\n"
                    "-Valores con formato -> 3E+05, 45.6\n"
                  )
        messagebox.showinfo('INFORMACION',mensaje)