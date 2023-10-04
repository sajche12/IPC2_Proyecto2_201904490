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
import graphviz, subprocess
from lista_mensajes_construir import ListaMensajesConstruir
from mensaje_construir import MensajeConstruir

lista_dron = ListaDrones()
lista_sistemas = ListaSistemas()
lista_mensajes_nuevos = ListaMensajes()
lista_drones_nombres = ListaDronesNombres()
lista_mensajes_construir = ListaMensajesConstruir()

#Metodo para inicializar el sistema
def inicializacion():
    #inicializar todas las listas creadas
    lista_dron.drones.clear()
    lista_sistemas.sistemas.clear()
    lista_mensajes_nuevos.mensajes.clear()
    lista_drones_nombres.drones_nombres.clear()
    lista_mensajes_construir.lista_mensajes_construir.clear()
    
    #Muestra mensaje de exito
    messagebox.showinfo("Inicializacion", "Inicializacion exitosa")
    
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
    # Creamos el elemento raíz
    root = ET.Element("respuesta")
    
    # Creamos los elementos hijos
    lista_mensajes = ET.SubElement(root, "listaMensajes")
    for i in lista_mensajes_construir.lista_mensajes_construir:
        mensaje = ET.SubElement(lista_mensajes, "mensaje")
        mensaje.set("nombre", i.nombre_mensaje)
        sistema = ET.SubElement(mensaje, "sistemaDrones")
        sistema.text = f"{i.sistema_drones}"
        tiempo = ET.SubElement(sistema, "tiempoOptimo")
        tiempo.text = f"{i.tiempo}"
        mensaje_recibido = ET.SubElement(sistema, "mensajeRecibido")
        mensaje_recibido.text = f"{i.mensaje}"
    
    # Creamos el archivo XML
    tree = ET.ElementTree(root)
    tree.write("respuesta.xml", encoding="utf-8", xml_declaration=True, short_empty_elements=False)
    
    
    messagebox.showinfo("Generar Archivo", "Archivo generado exitosamente")
    
    
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

    lista_ordenada = sorted(lista_drones_nombres.drones_nombres, key=lambda x: str(x.nombre_dron))
    for i in lista_ordenada:
        tabla_drones.insert("", END, text=f"{getattr(i, 'nombre_dron', 'NA')}")
    
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
    # Crear el grafo
    dot = graphviz.Digraph()

    altura_maxima = 0
    j = 1
    # Agregar los nodos al grafo
    for sistema in lista_sistemas.sistemas:
        dot.node(str(sistema.nombre), f"Nombre Sistema: {str(sistema.nombre)}" ,shape='box')
        altura_maxima = int(sistema.altura_max)
        dot.node("max", f"Altura maxima: {str(sistema.altura_max)}", shape='box', pos='0,1!')
        dot.node("cantidad", f"Cantidad drones: {str(sistema.cantidad_drones)}", shape='box', pos='0,2!')
        dot.node("Alturas", "Altura (mts)", shape='oval')
        for i in range(1, int(sistema.altura_max)+1):
            dot.node(str(i), str(i), shape='oval')
            if i == 1:
                dot.edge("Alturas", str(i))
            else:
                dot.edge(str(i-1), str(i))
        i = 1     
        for contenido in lista_dron.drones:
            if i == 1:
                dot.node(str(contenido.nombre), str(contenido.nombre), shape='oval')
                dot.node(f"1,{str(j)}", str(contenido.valor), shape='oval')
                dot.edge(str(contenido.nombre), f"1,{str(j)}")
            elif i > altura_maxima:
                i = 1
                dot.node(str(contenido.nombre), str(contenido.nombre), shape='oval')
                dot.node(f"1,{str(j)}", str(contenido.valor), shape='oval')
                dot.edge(str(contenido.nombre), f"1,{str(j)}")
            else:
                dot.node(f"1,{str(j)}", str(contenido.valor), shape='oval')
                dot.edge(f"1,{str(j-1)}", f"1,{str(j)}")
            i += 1
            j += 1
            
    # Renderizar el grafo
    dot.render('sistema_drones.dot', format='png', view=True)

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
    
    sistema_utilizar = ""
    for i in lista_mensajes_nuevos.mensajes:
        #Agregar i.nombre_mensaje a seleccion_mensaje pero si i.nombre_mensaje ya existe no agregarlo
        if i.nombre_mensaje not in seleccion_mensaje.get(0, END):
            seleccion_mensaje.insert(END, i.nombre_mensaje)
        sistema_utilizar = i.nombre_sistema
    
    #Boton seleccionar mensaje
    boton_seleccionar_mensaje = Button(marco, text="Siguiente", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: mostrar_nombre_sistema(seleccion_mensaje.get(seleccion_mensaje.curselection()), sistema_utilizar))
    boton_seleccionar_mensaje.place(x=25, y=300)
    
    #Boton volver
    boton_volver = Button(marco, text="Volver", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: volver_a_principal(seleccionar_mensaje))
    boton_volver.place(x=25, y=350)
    
    
def mostrar_nombre_sistema(mensaje_seleccionado, sistema_seleccionado):
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

    tiempo = 0
    for sistema in lista_sistemas.sistemas:
        if sistema_seleccionado == sistema.nombre:
            sistema_utilizar = Label(marco, text=f"Sistema a utilizar: {sistema_seleccionado}", font=("Skranji", 15), bg="#17202A", fg="#fff")
            sistema_utilizar.place(x=25, y=100)
            tiempo = sistema.altura_max
    
    mensaje_utilizar = Label(marco, text=f"Mensaje a utilizar: {mensaje_seleccionado}", font=("Skranji", 15), bg="#17202A", fg="#fff")
    mensaje_utilizar.place(x=25, y=150)
    
    tiempo_estimado = Label(marco, text=f"Tiempo estimado: {tiempo} segundos", font=("Skranji", 15), bg="#17202A", fg="#fff")
    tiempo_estimado.place(x=25, y=200)
    
    boton_siguiente = Button(marco, text="Siguiente", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: ver_listado_instrucciones_graphviz(mensaje_seleccionado, sistema_seleccionado, tiempo))
    boton_siguiente.place(x=25, y=250)

    #Boton volver
    boton_volver = Button(marco, text="Volver", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: volver_a_principal(mostrar_nombre_sistema))
    boton_volver.place(x=25, y=300)
    
def ver_listado_mensajes_instrucciones():
    mensajes_instrucciones = Toplevel(root)
    mensajes_instrucciones.title("Listado de Mensajes con Instrucciones")
    mensajes_instrucciones.geometry("900x500")
    #mensajes_instrucciones.resizable(False, False)
    
    # Obtener el tamaño de la pantalla
    pantalla_width = root.winfo_screenwidth()
    pantalla_height = root.winfo_screenheight()
    
    # Calcular la posición de la ventana para centrarla
    x = int((pantalla_width/2) - (900/2))
    y = int((pantalla_height/2) - (500/2))
    
    # Establecer la posición de la ventana
    mensajes_instrucciones.geometry(f"+{x}+{y}")
    mensajes_instrucciones.grab_set()
    mensajes_instrucciones.protocol("WM_DELETE_WINDOW", lambda: mensajes_instrucciones.destroy())
    
    root.withdraw()
    
    marco = Frame(mensajes_instrucciones, width=900, height=500)
    marco.config(bg="#17202A")
    marco.pack(fill="both", expand="True")
    
    #Titulo del proyecto
    titulo = Label(marco, text="LISTADO DE MENSAJES CON INSTRUCCIONES", font=("Skranji", 20), bg="#17202A", fg="#fff")
    titulo.place(x=20, y=20)
    
    #Tabla de mensajes con instrucciones
    tabla_mensajes = ttk.Treeview(marco, columns=("Dron", "Altura"))
    tabla_mensajes.heading("#0", text="Dron", anchor="center")
    tabla_mensajes.heading("#1", text="Altura", anchor="center")
    tabla_mensajes.place(x=10, y=100)
    tabla_mensajes.column("#0", anchor="center", width=150)
    tabla_mensajes.column("#1", anchor="center", width=150)
    
    lista_ordenada = sorted(lista_mensajes_nuevos.mensajes, key=lambda x: str(x.nombre_mensaje))
    for i in lista_ordenada:
        #verificar si existe un label con el mismo nombre de i.nombre_mensaje
        if i.nombre_mensaje:
            mensaje = Label(marco, text=f"Mensaje: {getattr(i, 'nombre_mensaje', 'NA')}", font=("Skranji", 15), bg="#17202A", fg="#fff")
            mensaje.place(x=25, y=60)
        tabla_mensajes.insert("", END, text=i.nombre_dron ,values=(i.altura_valor))
        
    #Boton volver
    boton_volver = Button(marco, text="Volver", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: volver_a_principal(mensajes_instrucciones))
    boton_volver.place(x=25, y=350)
    
def ver_listado_instrucciones_graphviz(mensaje, sistema, tiempo):
    # Crear el grafo
    dot = graphviz.Digraph()
    subir = "subir"
    bajar = "bajar"
    esperar = "esperar"
    emitir_luz = "emitir luz"
    
    dot.node("tiempo", "Tiempo (seg)", shape='box')
    for j in range(1, int(tiempo)+1):
        dot.node(str(j), str(j), shape='box')
        if j == 1:
            dot.edge("tiempo", str(j))
        else:
            dot.edge(str(j-1), str(j))
    
    cadena = ""
    z = 1
    for i, dron in enumerate(lista_dron.drones):
        if dron.nombre not in dot.body:
            dot.node(str(dron.nombre), str(dron.nombre), shape='box')
        else:
            break
        for msj in lista_mensajes_nuevos.mensajes:
            if str(msj.nombre_mensaje) == str(mensaje):
                if str(msj.nombre_dron) == str(dron.nombre) and str(msj.altura_valor) == str(dron.altura):
                    cadena += str(dron.valor)
                    dot.node(f"1,{str(z)}", str(emitir_luz), shape='box')
                    break
                else:
                    dot.node(f"1,{str(z)}", str(subir), shape='box')
                    continue
        if i == 0:
            dot.edge(str(dron.nombre), f"1,{str(z)}")
        else:
            dot.edge(f"1,{str(z-1)}", f"1,{str(z)}")
        z += 1
    
    mensaje_obtenido = MensajeConstruir(mensaje, sistema, tiempo, cadena)
    lista_mensajes_construir.lista_mensajes_construir.append(mensaje_obtenido)
    
    dot.render('instrucciones.dot', format='png', view=True)
    
def ver_instrucciones_para_mensaje():
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
    titulo = Label(marco, text="VER INSTRUCCIONES PARA VER MENSAJE", font=("Skranji", 15), bg="#17202A", fg="#fff")
    titulo.place(x=40, y=20)
    
    #Boton seleccionar mensaje
    boton_seleccionar_mensaje = Button(marco, text="Seleccionar Mensaje", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: seleccionar_mensaje())
    boton_seleccionar_mensaje.place(x=25, y=100)
    
    #Boton volver
    boton_volver = Button(marco, text="Volver", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: volver_a_principal(ver_instrucciones))
    boton_volver.place(x=25, y=150)
    
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
    boton_ver_listado_mensajes = Button(marco, text="Ver Listado de Mensajes y sus instrucciones", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: ver_listado_mensajes_instrucciones())
    boton_ver_listado_mensajes.place(x=25, y=100)
    
    #Boton ver instrucciones para ver mensaje
    boton_ver_instrucciones = Button(marco, text="Ver Instrucciones para ver Mensaje", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: ver_instrucciones_para_mensaje())
    boton_ver_instrucciones.place(x=25, y=150)
    
    #Boton volver
    boton_volver = Button(marco, text="Volver", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: volver_a_principal(gestion_mensajes))
    boton_volver.place(x=25, y=200)
    
#Metodo de ayuda
def ayuda():
    ayuda = Toplevel(root)
    ayuda.title("Ayuda")
    ayuda.geometry("500x500")
    ayuda.resizable(False, False)
    
    # Obtener el tamaño de la pantalla
    pantalla_width = root.winfo_screenwidth()
    pantalla_height = root.winfo_screenheight()
    
    # Calcular la posición de la ventana para centrarla
    x = int((pantalla_width/2) - (500/2))
    y = int((pantalla_height/2) - (500/2))
    
    # Establecer la posición de la ventana
    ayuda.geometry(f"+{x}+{y}")
    ayuda.grab_set()
    ayuda.protocol("WM_DELETE_WINDOW", lambda: ayuda.destroy())
    
    root.withdraw()
    
    marco = Frame(ayuda, width=500, height=500)
    marco.config(bg="#17202A")
    marco.pack(fill="both", expand="True")
    
    #Titulo del proyecto
    titulo = Label(marco, text="AYUDA", font=("Skranji", 20), bg="#17202A", fg="#fff")
    titulo.place(x=180, y=20)
    
    #Label de nombre
    nombre = Label(marco, text="Nombre: Diego Aldair Sajche Avila", font=("Skranji", 15), bg="#17202A", fg="#fff")
    nombre.place(x=25, y=100)
    
    #Label de carnet
    carnet = Label(marco, text="Carnet: 201904490", font=("Skranji", 15), bg="#17202A", fg="#fff")
    carnet.place(x=25, y=150)
    
    #Label de curso
    curso = Label(marco, text="Curso: IPC2 - Seccion D", font=("Skranji", 15), bg="#17202A", fg="#fff")
    curso.place(x=25, y=200)
    
    #Label de proyecto
    proyecto = Label(marco, text="Proyecto No. 2", font=("Skranji", 15), bg="#17202A", fg="#fff")
    proyecto.place(x=25, y=250)
    
    # agregar link hacia documentacion
    ruta_pdf = "C:/Users/ACER/Documents/GitHub/IPC2_Proyecto2_201904490/Documentacion/Documentacion.pdf"
    
    # Label de documentacion
    documentacion = Label(marco, text="Click aqui para ver la documentacion", font=("Skranji", 15), bg="#17202A", fg="#fff", cursor="hand2")
    documentacion.place(x=25, y=300)
    
    #Asociar documentacion con link
    documentacion.bind("<Button-1>", lambda e: subprocess.Popen([r"C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat\Acrobat.exe", ruta_pdf]))
    
    #Boton volver
    boton_volver = Button(marco, text="Volver", font=("Skranji", 15), bg="#17202A", fg="#fff", command=lambda: volver_a_principal(ayuda))
    boton_volver.place(x=25, y=350)

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
    
    