class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
         
class LinkedList:
    def __init__(self):
        self.head = None
    def push(self, new_data):
        new_node = Node(new_data)
        new_node.next = self.head
        self.head = new_node
         
    def printList(self):
        n = self.head
        while n:
            print(n.data, end=' ')
            n = n.next
        print()