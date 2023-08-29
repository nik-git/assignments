"""
Linked List classes
"""
class Node():
    """
    Node Class
    """
    def __init__(self, data=None, next_node=None) -> None:
        self.data = data
        self.next_node = next_node

class LinkedList():
    """
    Linked List class
    """
    def __init__(self) -> None:
        self.head = None

    def add_in_start(self, data):
        """
        Add in start
        """
        new_node = Node(data, self.head)
        self.head = new_node

    def add_in_end(self, data):
        """
        Add in End
        """
        node = Node(data, None)
        ptr = self.head
        while ptr.next_node:
            ptr = ptr.next_node
        ptr.next_node = node


    def print_ll(self):
        """
        print LL
        """
        # print("111111")
        # print(self.head.data)
        ptr = self.head
        while ptr:
            print(ptr.data)
            # print("=>")
            ptr = ptr.next_node
    
    def rev(self):
        """
        sdfs
        """
        previous = None
        current = self.head
        after = current.next_node
        while current:
            current.next_node = previous
            previous = current
            current = after
            if after:
                after = after.next_node
        self.head = previous


ll = LinkedList()
ll.add_in_start(2)
ll.add_in_start(4)
ll.add_in_start(6)
ll.add_in_end(8)
ll.print_ll()
print("======================")
ll.rev()
ll.print_ll()


# ll.print_ll()