class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
    
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
    def sort(self):
        current = self.head
        index = None
        if self.head is None:
            return
        else:
            while current is not None:
                index = current.next
                while index is not None:
                    if current.data > index.data:
                        temp = current.data
                        current.data = index.data
                        index.data = temp
                    index = index.next
                current = current.next
    