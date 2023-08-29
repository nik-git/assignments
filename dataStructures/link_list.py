"""
Linked List
"""
class Node:
    """
    Node class
    """
    def __init__(self, data=None, next_node=None) -> None:
        self.data = data
        self.next_node = next_node

class LinkedList:
    """
    Linked List
    """
    def __init__(self) -> None:
        self.head = None

    def insert_at_begining(self, data):
        """
        Insert data in the start of the Linked List
        """
        node = Node(data, self.head)
        self.head = node

    def insert_at_end(self, data):
        """
        Insert at end
        """
        node = Node(data, None)
        ptr = self.head
        while ptr.next_node:
            # if ptr.next_node is None:
            ptr = ptr.next_node
        ptr.next_node = node

    def del_from_end(self):
        """
        Del in end
        """
        if self.head:
            ptr = self.head
            while ptr.next_node:
                ptr = ptr.next_node
            print(ptr.data)


    def print_linked_list(self):
        """
        Print all elements of the linked list
        """
        ptr = self.head
        while ptr:
            print(ptr.data, end="")
            print("==>", end="")
            ptr = ptr.next_node

if __name__ == "__main__":
    ll = LinkedList()
    ll.insert_at_begining(5)
    ll.insert_at_begining(10)
    ll.insert_at_begining(15)
    ll.insert_at_begining(20)
    ll.insert_at_end(4)
    ll.insert_at_end(3)
    ll.insert_at_end(2)
    ll.del_from_end()
    ll.print_linked_list()
