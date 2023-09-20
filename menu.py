from tkinter import *
from tkinter import messagebox, filedialog
from dron import Dron
from sistema_drones import SistemaDrones
from mensaje import Mensaje
from lista_drones import ListaDrones
from lista_sistemas import ListaSistemas
from lista_mensajes import ListaMensajes
import xml.etree.ElementTree as ET


#Metodo para inicializar el sistema
def inicializacion():
    print("Inicializacion")
    
#Metodo para cargar archivo
def cargar_archivo():
    #cargar archivo xml desde el explorador de archivos
    archivo = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
    
    tree = ET.parse(archivo)
    root = tree.getroot()
    
    #Lista de drones
    for dron in root.find('listaDrones'):
        nombre = dron.text
        print(f"Nombre: {nombre}")
        for datos in root.find('listaSistemasDrones/sistemaDrones/contenido'):
            if datos.text == nombre:
                for altura in root.find('listaSistemasDrones/sistemaDrones/contenido/alturas'):
                    altura_dron = altura.attrib['valor']
                    print(f"Altura: {altura_dron}")
                    valor = altura.text
                    print(f"Valor: {valor}")
                    dron_nuevo = Dron(nombre, altura_dron, valor)
    
#Metodo para generar archivo de salida
def generar_archivo():
    print("Generar archivo de salida")
    
#Metodo para gestion de drones
def gestion_drones():
    print("Gestion de drones")
    
#Metodo para gestion de sistema de drones
def sistema_drones():
    print("Gestion sistema de drones")
    
#Metodo para gestion de mensajes
def gestion_mensajes():
    print("Gestion de mensajes")

#Metodo de ayuda
def ayuda():
    messagebox.showinfo("Ayuda", "Diego Aldair Sajche Avila\n201904490\nIPC2 - Seccion D\nProyecto 2\nAqui el link hacia documentacion")


root = Tk()
root.title("Menu")
root.geometry("500x500")
root.resizable(False, False)

# Obtener el tamaño de la pantalla
pantalla_width = root.winfo_screenwidth()
pantalla_height = root.winfo_screenheight()

# Calcular la posición de la ventana para centrarla
x = int((pantalla_width/2) - (500/2))
y = int((pantalla_height/2) - (500/2))

# Establecer la posición de la ventana
root.geometry(f"+{x}+{y}")

marco = Frame(root, width=500, height=500)
marco.config(bg="#17202A")
marco.pack(fill="both", expand="True")

#Titulo del proyecto
titulo = Label(marco, text="SISTEMA DE DRONES", font=("Skranji", 20), bg="#17202A", fg="#fff")
titulo.place(x=100, y=20)

#Boton Inicializacion
boton_inicializacion = Button(marco, text="Inicializacion", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: inicializacion())
boton_inicializacion.place(x=25, y=100)

#Boton cargar archivo
boton_cargar_archivo = Button(marco, text="Cargar Archivo", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: cargar_archivo())
boton_cargar_archivo.place(x=25, y=150)

#Boton generar archivo de salida
boton_generar_archivo = Button(marco, text="Generar Archivo de Salida", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: generar_archivo())
boton_generar_archivo.place(x=25, y=200)

#Boton gestion de drones
boton_gestion_drones = Button(marco, text="Gestion de Drones", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: gestion_drones())
boton_gestion_drones.place(x=25, y=250)

#Boton gestion sistema de drones
boton_sistema_drones = Button(marco, text="Gestion Sistema de Drones", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: sistema_drones())
boton_sistema_drones.place(x=25, y=300)

#Boton gestion de mensajes
boton_gestion_mensajes = Button(marco, text="Gestion de Mensajes", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: gestion_mensajes())
boton_gestion_mensajes.place(x=25, y=350)

#Boton ayuda
boton_ayuda = Button(marco, text="Ayuda", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: ayuda())
boton_ayuda.place(x=25, y=400)

root.mainloop()
    
    