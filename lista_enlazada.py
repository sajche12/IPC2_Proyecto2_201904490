class Nodo:
    def __init__(self, valor, siguiente=None):
        self.valor = valor
        self.siguiente = siguiente

    def __str__(self):
        return str(self.valor)
    
class ListaEnlazada:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.len = 0
        
    #Metodo para agregar un elemento al final de la lista
    def agregar_nodo(self, valor):
        nuevo = Nodo(valor)
        if self.primero == None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            self.ultimo = nuevo
        self.len += 1
    
    #Metodo para volver iterable la lista
    def __iter__(self):
        actual = self.primero
        while actual!= None:
            yield actual
            actual = actual.siguiente

    #Metodo para obtener el tamaño de la lista
    def __len__(self):
        return self.len
    