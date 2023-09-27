from tkinter import *
from tkinter import messagebox, filedialog, ttk
from dron import Dron
from sistema_drones import SistemaDrones
from mensaje import Mensaje
from lista_drones import ListaDrones
from lista_sistemas import ListaSistemas
from lista_mensajes import ListaMensajes
import xml.etree.ElementTree as ET
from lista_dron_nombre import ListaDronesNombres
from dron_nombre import DronNombre

lista_dron = ListaDrones()
lista_sistemas = ListaSistemas()
lista_mensajes_nuevos = ListaMensajes()
lista_drones_nombres = ListaDronesNombres()

#Metodo para inicializar el sistema
def inicializacion():
    print("Inicializacion")
    
#Metodo para cargar archivo
def cargar_archivo():
    #cargar archivo xml desde el explorador de archivos
    archivo = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
    
    tree = ET.parse(archivo)
    root = tree.getroot()
    
    # Accede a la lista de drones
    lista_drones = root.find('listaDrones')

    # Accede a la lista de sistemas de drones
    lista_sistemas_drones = root.find('listaSistemasDrones')

    # Accede a la lista de mensajes
    lista_mensajes = root.find('listaMensajes')
    
    # Recorre la lista de drones
    for dron in lista_drones:
        nombre = dron.text
        nombre_nuevo = DronNombre(nombre)
        lista_drones_nombres.drones_nombres.append(nombre_nuevo)
        

    # Recorre la lista de sistemas de drones
    for sistema_drones in lista_sistemas_drones.findall('sistemaDrones'):
        nombre = sistema_drones.get('nombre')
        altura_maxima = sistema_drones.find('alturaMaxima').text
        cantidad_drones = sistema_drones.find('cantidadDrones').text
        sistema_drones_nuevo = SistemaDrones(nombre, altura_maxima, cantidad_drones)
        lista_sistemas.sistemas.append(sistema_drones_nuevo)
        for dron in sistema_drones.findall('contenido'):
            nombre_dron = dron.find('dron').text
            alturas = dron.find('alturas')
            for altura in alturas.findall('altura'):
                valor = altura.get('valor')
                letra = altura.text
                dron_nuevo = Dron(nombre_dron, valor, letra)
                lista_dron.drones.append(dron_nuevo)
            
    # Recorre la lista de mensajes
    for mensaje in lista_mensajes.findall('Mensaje'):
        nombre_mensaje = mensaje.get('nombre')
        sistema_drones = mensaje.find('sistemaDrones').text
        instrucciones = mensaje.find('instrucciones')
        for instruccion in instrucciones:
            dron = instruccion.get('dron')
            valor = instruccion.text
            mensaje_nuevo = Mensaje(nombre_mensaje, sistema_drones, dron, valor)
            lista_mensajes_nuevos.mensajes.append(mensaje_nuevo)
    
    #Muestra mensaje de exito
    messagebox.showinfo("Cargar Archivo", "Archivo cargado exitosamente")
#Metodo para generar archivo de salida
def generar_archivo():
    print("Generar archivo de salida")

def ver_listado_drones():
    listado_drones = Toplevel(root)
    listado_drones.title("Listado de Drones")
    listado_drones.geometry("500x500")
    listado_drones.resizable(False, False)
    
    # Obtener el tamaño de la pantalla
    pantalla_width = root.winfo_screenwidth()
    pantalla_height = root.winfo_screenheight()
    
    # Calcular la posición de la ventana para centrarla
    x = int((pantalla_width/2) - (500/2))
    y = int((pantalla_height/2) - (500/2))
    
    # Establecer la posición de la ventana
    listado_drones.geometry(f"+{x}+{y}")
    listado_drones.grab_set()
    listado_drones.protocol("WM_DELETE_WINDOW", lambda: listado_drones.destroy())
    
    root.withdraw()
    
    marco = Frame(listado_drones, width=500, height=500)
    marco.config(bg="#17202A")
    marco.pack(fill="both", expand="True")
    
    #Titulo del proyecto
    titulo = Label(marco, text="LISTADO DE DRONES", font=("Skranji", 20), bg="#17202A", fg="#fff")
    titulo.place(x=100, y=20)
    
    #Tabla de drones
    tabla_drones = ttk.Treeview(marco, columns=("Nombre"))
    tabla_drones.heading("#0", text="Nombre")
    tabla_drones.place(x=25, y=100)
    tabla_drones.column("#0", anchor="center")

    #lista_drones_nombres.drones_nombres.sort()
    for i in lista_drones_nombres.drones_nombres:
        tabla_drones.insert("", END, text=i.nombre_dron)
    
    #Agregar scroll a la tabla
    scroll = ttk.Scrollbar(marco, orient="vertical", command=tabla_drones.yview)
    scroll.place(x=400, y=100, height=200)
    tabla_drones.configure(yscrollcommand=scroll.set)
    
    #Boton volver
    boton_volver = Button(marco, text="Volver", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: volver_a_principal(listado_drones))
    boton_volver.place(x=25, y=350)

def agregar_dron_lista(nombre_dron):
    #verificar si nombre_dron se encuentra en lista_drones_nombres.drones_nombres
    if nombre_dron in lista_drones_nombres.drones_nombres:
        messagebox.showerror("Agregar Nuevo Dron", "El nombre del dron ya existe")
    else:
        #agregar nombre_dron a lista_drones_nombres.drones_nombres
        nombre_nuevo = DronNombre(nombre_dron)
        lista_drones_nombres.drones_nombres.append(nombre_nuevo)
        messagebox.showinfo("Agregar Nuevo Dron", "Dron agregado exitosamente")
    

def agregar_nuevo_dron():
    agregar_dron = Toplevel(root)
    agregar_dron.title("Agregar Nuevo Dron")
    agregar_dron.geometry("500x500")
    agregar_dron.resizable(False, False)
    
    # Obtener el tamaño de la pantalla
    pantalla_width = root.winfo_screenwidth()
    pantalla_height = root.winfo_screenheight()
    
    # Calcular la posición de la ventana para centrarla
    x = int((pantalla_width/2) - (500/2))
    y = int((pantalla_height/2) - (500/2))
    
    # Establecer la posición de la ventana
    agregar_dron.geometry(f"+{x}+{y}")
    agregar_dron.grab_set()
    agregar_dron.protocol("WM_DELETE_WINDOW", lambda: agregar_dron.destroy())
    
    root.withdraw()
    
    marco = Frame(agregar_dron, width=500, height=500)
    marco.config(bg="#17202A")
    marco.pack(fill="both", expand="True")
    
    #Titulo del proyecto
    titulo = Label(marco, text="AGREGAR NUEVO DRON", font=("Skranji", 20), bg="#17202A", fg="#fff")
    titulo.place(x=100, y=20)
    
    #Nombre del dron
    nombre_dron = Label(marco, text="Nombre del Dron:", font=("Skranji", 15), bg="#17202A", fg="#fff")
    nombre_dron.place(x=25, y=100)
    
    #Campo de texto para el nombre del dron
    campo_nombre_dron = Entry(marco, width=30)
    campo_nombre_dron.place(x=25, y=150)
    
    #Boton agregar dron
    boton_agregar_dron = Button(marco, text="Agregar Dron", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: agregar_dron_lista(campo_nombre_dron.get()))
    boton_agregar_dron.place(x=25, y=200)
    
    #Boton volver
    boton_volver = Button(marco, text="Volver", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: volver_a_principal(agregar_dron))
    boton_volver.place(x=25, y=250)
    
#Metodo para gestion de drones
def gestion_drones():
    gestion_drones = Toplevel(root)
    gestion_drones.title("Gestion de Drones")
    gestion_drones.geometry("500x500")
    gestion_drones.resizable(False, False)

    # Obtener el tamaño de la pantalla
    pantalla_width = root.winfo_screenwidth()
    pantalla_height = root.winfo_screenheight()

    # Calcular la posición de la ventana para centrarla
    x = int((pantalla_width/2) - (500/2))
    y = int((pantalla_height/2) - (500/2))

    # Establecer la posición de la ventana
    gestion_drones.geometry(f"+{x}+{y}")
    gestion_drones.grab_set()
    gestion_drones.protocol("WM_DELETE_WINDOW", lambda: gestion_drones.destroy())
    
    root.withdraw()
    
    marco = Frame(gestion_drones, width=500, height=500)
    marco.config(bg="#17202A")
    marco.pack(fill="both", expand="True")

    #Titulo del proyecto
    titulo = Label(marco, text="GESTION DE DRONES", font=("Skranji", 20), bg="#17202A", fg="#fff")
    titulo.place(x=100, y=20)
    
    #Boton ver listado de drones
    boton_ver_listado_drones = Button(marco, text="Ver Listado de Drones", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: ver_listado_drones())
    boton_ver_listado_drones.place(x=25, y=100)
    
    #Boton agregar nuevo dron
    boton_agregar_nuevo_dron = Button(marco, text="Agregar Nuevo Dron", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: agregar_nuevo_dron())
    boton_agregar_nuevo_dron.place(x=25, y=150)
    
    #Boton volver
    boton_volver = Button(marco, text="Volver", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: volver_a_principal(gestion_drones))
    boton_volver.place(x=25, y=200)
def volver_a_principal(ventana):
    ventana.destroy()
    root.deiconify()
    
def ver_listado_sistemas():
    pass
#Metodo para gestion de sistema de drones
def gestion_sistema_drones():
    gestion_sistema = Toplevel(root)
    gestion_sistema.title("Gestion de Sistema de Drones")
    gestion_sistema.geometry("500x500")
    gestion_sistema.resizable(False, False)
    
    # Obtener el tamaño de la pantalla
    pantalla_width = root.winfo_screenwidth()
    pantalla_height = root.winfo_screenheight()

    # Calcular la posición de la ventana para centrarla
    x = int((pantalla_width/2) - (500/2))
    y = int((pantalla_height/2) - (500/2))

    # Establecer la posición de la ventana
    gestion_sistema.geometry(f"+{x}+{y}")
    gestion_sistema.grab_set()
    gestion_sistema.protocol("WM_DELETE_WINDOW", lambda: gestion_sistema.destroy())
    
    root.withdraw()
    
    marco = Frame(gestion_sistema, width=500, height=500)
    marco.config(bg="#17202A")
    marco.pack(fill="both", expand="True")

    #Titulo del proyecto
    titulo = Label(marco, text="GESTION DE SISTEMA DE DRONES", font=("Skranji", 20), bg="#17202A", fg="#fff")
    titulo.place(x=15, y=20)
    
    #Boton ver listado de sistemas de drones
    boton_ver_listado_sistemas = Button(marco, text="Ver Listado de Sistemas de Drones", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: ver_listado_sistemas())
    boton_ver_listado_sistemas.place(x=25, y=100)
    
    #Boton volver
    boton_volver = Button(marco, text="Volver", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: volver_a_principal(gestion_sistema))
    boton_volver.place(x=25, y=150)
    
def ver_listado_mensajes():
    pass

def seleccionar_mensaje():
    seleccionar_mensaje = Toplevel(root)
    seleccionar_mensaje.title("Seleccionar Mensaje")
    seleccionar_mensaje.geometry("500x500")
    seleccionar_mensaje.resizable(False, False)
    
    # Obtener el tamaño de la pantalla
    pantalla_width = root.winfo_screenwidth()
    pantalla_height = root.winfo_screenheight()

    # Calcular la posición de la ventana para centrarla
    x = int((pantalla_width/2) - (500/2))
    y = int((pantalla_height/2) - (500/2))

    # Establecer la posición de la ventana
    seleccionar_mensaje.geometry(f"+{x}+{y}")
    seleccionar_mensaje.grab_set()
    seleccionar_mensaje.protocol("WM_DELETE_WINDOW", lambda: seleccionar_mensaje.destroy())
    
    root.withdraw()
    
    marco = Frame(seleccionar_mensaje, width=500, height=500)
    marco.config(bg="#17202A")
    marco.pack(fill="both", expand="True")

    #Titulo del proyecto
    titulo = Label(marco, text="SELECCIONA UN MENSAJE:", font=("Skranji", 20), bg="#17202A", fg="#fff")
    titulo.place(x=80, y=20)

    seleccion_mensaje = Listbox(marco, width=50, height=10)
    seleccion_mensaje.place(x=25, y=100)
    
    for i in lista_mensajes_nuevos.mensajes:
        seleccion_mensaje.insert(END, i.nombre_sistema)
    
    #Boton seleccionar mensaje
    boton_seleccionar_mensaje = Button(marco, text="Siguiente", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: mostrar_nombre_sistema(seleccion_mensaje.get(seleccion_mensaje.curselection())))
    boton_seleccionar_mensaje.place(x=25, y=300)
    
    
def mostrar_nombre_sistema(mensaje_seleccionado):
    mostrar_nombre_sistema = Toplevel(root)
    mostrar_nombre_sistema.title("Mostrar Nombre de Sistema de Drones")
    mostrar_nombre_sistema.geometry("500x500")
    mostrar_nombre_sistema.resizable(False, False)
    
    # Obtener el tamaño de la pantalla
    pantalla_width = root.winfo_screenwidth()
    pantalla_height = root.winfo_screenheight()

    # Calcular la posición de la ventana para centrarla
    x = int((pantalla_width/2) - (500/2))
    y = int((pantalla_height/2) - (500/2))

    # Establecer la posición de la ventana
    mostrar_nombre_sistema.geometry(f"+{x}+{y}")
    mostrar_nombre_sistema.grab_set()
    mostrar_nombre_sistema.protocol("WM_DELETE_WINDOW", lambda: mostrar_nombre_sistema.destroy())
    
    root.withdraw()
    
    marco = Frame(mostrar_nombre_sistema, width=500, height=500)
    marco.config(bg="#17202A")
    marco.pack(fill="both", expand="True")

    #Titulo del proyecto
    titulo = Label(marco, font=("Skranji", 20), bg="#17202A", fg="#fff")
    titulo.place(x=80, y=20)

    sistema_utilizar = Label(marco, text="Sistema a utilizar:", font=("Skranji", 15), bg="#17202A", fg="#fff")
    sistema_utilizar.place(x=25, y=100)
    
    mensaje_utilizar = Label(marco, text=f"Mensaje a utilizar: {mensaje_seleccionado}", font=("Skranji", 15), bg="#17202A", fg="#fff")
    mensaje_utilizar.place(x=25, y=150)
    
    tiempo_estimado = Label(marco, text="Tiempo estimado:", font=("Skranji", 15), bg="#17202A", fg="#fff")
    tiempo_estimado.place(x=25, y=200)
    
    boton_siguiente = Button(marco, text="Siguiente", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: ver_listado_instrucciones())
    boton_siguiente.place(x=25, y=250)
    
def ver_listado_instrucciones():
    pass
def ver_instrucciones():
    ver_instrucciones = Toplevel(root)
    ver_instrucciones.title("Ver Instrucciones")
    ver_instrucciones.geometry("500x500")
    ver_instrucciones.resizable(False, False)
    
    # Obtener el tamaño de la pantalla
    pantalla_width = root.winfo_screenwidth()
    pantalla_height = root.winfo_screenheight()

    # Calcular la posición de la ventana para centrarla
    x = int((pantalla_width/2) - (500/2))
    y = int((pantalla_height/2) - (500/2))

    # Establecer la posición de la ventana
    ver_instrucciones.geometry(f"+{x}+{y}")
    ver_instrucciones.grab_set()
    ver_instrucciones.protocol("WM_DELETE_WINDOW", lambda: ver_instrucciones.destroy())
    
    root.withdraw()
    
    marco = Frame(ver_instrucciones, width=500, height=500)
    marco.config(bg="#17202A")
    marco.pack(fill="both", expand="True")

    #Titulo del proyecto
    titulo = Label(marco, text="VER INSTRUCCIONES PARA VER MENSAJE", font=("Skranji", 20), bg="#17202A", fg="#fff")
    titulo.place(x=80, y=20)
    
    #Boton seleccionar mensaje
    boton_seleccionar_mensaje = Button(marco, text="Seleccionar Mensaje", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: seleccionar_mensaje())
    boton_seleccionar_mensaje.place(x=25, y=100)
    
    #Boton mostrar nombre de sistema de drones
    boton_mostrar_nombre_sistema = Button(marco, text="Mostrar Nombre de Sistema de Drones", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: mostrar_nombre_sistema())
    boton_mostrar_nombre_sistema.place(x=25, y=150)
    
    #Boton ver listado de instrucciones
    boton_ver_listado_instrucciones = Button(marco, text="Ver Listado de Instrucciones (Grafica)", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: ver_listado_instrucciones())
    boton_ver_listado_instrucciones.place(x=25, y=200)
    
    #Boton volver
    boton_volver = Button(marco, text="Volver", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: volver_a_principal(ver_instrucciones))
    boton_volver.place(x=25, y=250)
    
#Metodo para gestion de mensajes
def gestion_mensajes():
    gestion_mensajes = Toplevel(root)
    gestion_mensajes.title("Gestion de Mensajes")
    gestion_mensajes.geometry("500x500")
    gestion_mensajes.resizable(False, False)
    
    # Obtener el tamaño de la pantalla
    pantalla_width = root.winfo_screenwidth()
    pantalla_height = root.winfo_screenheight()

    # Calcular la posición de la ventana para centrarla
    x = int((pantalla_width/2) - (500/2))
    y = int((pantalla_height/2) - (500/2))

    # Establecer la posición de la ventana
    gestion_mensajes.geometry(f"+{x}+{y}")
    gestion_mensajes.grab_set()
    gestion_mensajes.protocol("WM_DELETE_WINDOW", lambda: gestion_mensajes.destroy())
    
    root.withdraw()
    
    marco = Frame(gestion_mensajes, width=500, height=500)
    marco.config(bg="#17202A")
    marco.pack(fill="both", expand="True")

    #Titulo del proyecto
    titulo = Label(marco, text="GESTION DE MENSAJES", font=("Skranji", 20), bg="#17202A", fg="#fff")
    titulo.place(x=80, y=20)
    
    #Boton ver listado de mensajes
    boton_ver_listado_mensajes = Button(marco, text="Ver Listado de Mensajes e instrucciones", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: ver_listado_mensajes())
    boton_ver_listado_mensajes.place(x=25, y=100)
    
    #Boton ver instrucciones para ver mensaje
    boton_ver_instrucciones = Button(marco, text="Ver Instrucciones para ver Mensaje", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: ver_instrucciones())
    boton_ver_instrucciones.place(x=25, y=150)
    
    #Boton volver
    boton_volver = Button(marco, text="Volver", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: volver_a_principal(gestion_mensajes))
    boton_volver.place(x=25, y=200)
    
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
boton_sistema_drones = Button(marco, text="Gestion Sistema de Drones", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: gestion_sistema_drones())
boton_sistema_drones.place(x=25, y=300)

#Boton gestion de mensajes
boton_gestion_mensajes = Button(marco, text="Gestion de Mensajes", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: gestion_mensajes())
boton_gestion_mensajes.place(x=25, y=350)

#Boton ayuda
boton_ayuda = Button(marco, text="Ayuda", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: ayuda())
boton_ayuda.place(x=25, y=400)

#Boton salir
boton_salir = Button(marco, text="Salir", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: root.destroy())
boton_salir.place(x=25, y=450)

root.mainloop()
    
    