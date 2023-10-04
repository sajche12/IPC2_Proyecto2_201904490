class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.nombre_dron = ""
    
class LinkedList:
    def __init__(self):
        self.head = None
        
    #Metodo para agregar un elemento al final de la lista
    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node
        
    #Metodo para iterar la lista
    def __iter__(self):
        node = self.head
        while node:
            yield node.data
            node = node.next
            
    #Metodo para ordenar la lista
    def ordenar_alfabeticamente(self, atributo):
        if self.head is None:
            return
        actual = self.head
        while actual.next is not None:
            next = actual.next
            while next is not None and getattr(actual, atributo) > getattr(next, atributo):
                actual = next
                next = next.next
            if next is None:
                break
            actual.next = next.next
            next.next = actual

    #Metodo para borrar todos los nodos de la lista
    def clear(self):
        self.head = None
        