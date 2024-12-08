from typing import List, Any, Dict, Set, Generator

class StaticArray:
    def __init__(self, capacity: int):
        """
        Initialize a static array of a given capacity.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        self.capacity = capacity
        self.arr = [None] * capacity 

    def set(self, index: int, value: int) -> None:
        """
        Set the value at a particular index.
        """
        if not (0 <= index < self.capacity):
            raise IndexError("Index out of bounds.")
        self.arr[index] = value

    def get(self, index: int) -> int:
        """
        Retrieve the value at a particular index.
        """
        if not (0 <= index < self.capacity):
            raise IndexError("Index out of bounds.")
        value = self.arr[index]
        if value is None:
            raise ValueError("No value set at the specified index.")
        return value


class DynamicArray:
    def __init__(self):
        """
        Initialize an empty dynamic array.
        """
        self.size = 0 
        self.capacity = 1
        self.arr = [0]*self.capacity 

    def append(self, value: int) -> None:
        """
        Add a value to the end of the dynamic array.
        """
        if self.size == self.capacity: 
            self._resize()
        self.arr[self.size] = value 
        self.size += 1


    def insert(self, index: int, value: int) -> None:
        """
        Insert a value at a particular index.
        """
        if not (0 <= index <= self.size):
            raise IndexError("Index out of bounds.")
        if self.size == self.capacity: 
            self.resize() 
        for j in range(self.size, index, -1): 
            self.arr = self.arr[j-1]
        self.arr[index] = value 
        self.size += 1
        

    def delete(self, index: int) -> None:
        """
        Delete the value at a particular index.
        """
        if not (0 <= index < self.size):
            raise IndexError("Index out of bounds.")
        for j in range(index, self.size-1): 
            self.arr[j] = self.arr[j+1] 
        self.size -= 1 

    def get(self, index: int) -> int:
        """
        Retrieve the value at a particular index.
        """
        if not (0 <= index < self.size):
            raise IndexError("Index out of bounds.")
        return self.arr[index]
    
    def _resize(self): 
        """
        Resize array to capacity 'capacity'.
        """
        self.capacity = 2*self.capacity
        new_arr = [0]*self.capacity 

        for i in range(self.size): 
            new_arr[i] = self.arr[i]
        self.arr = new_arr  



class Node:
    def __init__(self, value: int):
        """
        Initialize a node.
        """
        self.value = value 
        self.next = None 

class SinglyLinkedList:
    def __init__(self):
        """
        Initialize an empty singly linked list.
        """
        self.head = None 
        self.tail = None 
        self.length = 0 

    def append(self, value: int) -> None:
        """
        Add a node with a value to the end of the linked list.
        """
        node = Node(value)
        if not self.head: 
            self.head = node 
            self.tail = node 
        else: 
            self.tail.next = node 
            self.tail = node
        self.length += 1  


    def insert(self, position: int, value: int) -> None:
        """
        Insert a node with a value at a particular position.
        """
        if position < 0 or (position > self.length): 
            return 
        
        curr = self.head 
        node = Node(value)
        # insert at head 
        if position == 0: 
            if self.length == 0: 
                self.head = node 
                self.tail = node 
            else:  
                node.next = self.head 
                self.head = node 
            self.length += 1
        # insert at tail 
        elif position == self.length:
            self.append(value) 
        else:
            n = position 
            while n > 1: 
                curr = curr.next 
                n -= 1
            node.next = curr.next 
            curr.next = node 
            self.length += 1
         

    def delete(self, value: int) -> None:
        """
        Delete the first node with a specific value.
        """
        if not self.head: 
            return 
        
        # delete at head  
        if self.head.value == value:
            if self.length == 1:
                self.head = None 
                self.tail = None 
            else:   
                self.head = self.head.next 
        else: 
            curr = self.head 
            prev = curr 
            while curr: 
                if curr.value == value:
                    prev.next = curr.next 
                    # if delete at tail 
                    if not prev.next:
                        self.tail = prev  
                    self.length -= 1
                    return 
                prev = curr 
                curr = curr.next  
        self.length -= 1 


    def find(self, value: int) -> Node:
        """
        Find a node with a specific value.
        """
        curr = self.head 
        while curr: 
            if curr.value == value: 
                return curr 
            curr = curr.next
        return None    

    def size(self) -> int:
        """
        Returns the number of elements in the linked list.
        """
        return self.length 

    def is_empty(self) -> bool:
        """
        Checks if the linked list is empty.
        """
        return self.length == 0

    def print_list(self) -> None:
        """
        Prints all elements in the linked list.
        """
        curr = self.head 
        while curr: 
            print(curr.value)
            curr = curr.next 
            

    def reverse(self) -> None:
        """
        Reverse the linked list in-place.
        """
        self.tail = self.head 
        curr = self.head 
        prev = None 
        while curr: 
            temp = curr.next 
            curr.next = prev 
            prev = curr 
            curr = temp 
        self.head = prev  
    
    def get_head(self) -> Node:
        """
        Returns the head node of the linked list.
        """
        return self.head 
    
    def get_tail(self) -> Node:
        """
        Returns the tail node of the linked list.
        """
        return self.tail 
    


class DoubleNode:
    def __init__(self, value: int, next_node = None, prev_node = None):
        """
        Initialize a double node with value, next, and previous.
        """
        self.value = value 
        self.prev = prev_node 
        self.next = next_node 

class DoublyLinkedList:
    def __init__(self):
        """
        Initialize an empty doubly linked list.
        """
        self.head = None 
        self.tail = None 
        self.length = 0 

    def append(self, value: int) -> None:
        """
        Add a node with a value to the end of the linked list.
        """
        node = DoubleNode(value)
        if self.length == 0: 
            self.head = node 
            self.tail = node 
        else: 
            self.tail.next = node 
            node.prev = self.tail 
            self.tail = node 
        self.length += 1


    def insert(self, position: int, value: int) -> None:
        """
        Insert a node with a value at a particular position.
        """
        if position < 0 or position > self.length: 
            return 
        
        node = DoubleNode(value)
        curr = self.head 
        # insert at head 
        if position == 0:
            if self.length == 0: 
                self.head = node 
                self.tail = node 
            else: 
                node.next = self.head 
                self.head.prev = node 
                self.head = node  
            self.length += 1 
        # insert at tail 
        elif position == self.length: 
            self.append(value)
        else: 
            for _ in range(position): 
                curr = curr.next 
            node.prev = curr.prev 
            node.next = curr 
            curr.prev.next = node 
            curr.prev = node 
            self.length += 1
        

    def delete(self, value: int) -> None:
        """
        Delete the first node with a specific value.
        """
        if not self.head: 
            return 
        
        # delete at head 
        if self.head.value == value:
            if self.length == 1: 
                self.head = None 
                self.tail = None 
            else:  
                self.head = self.head.next 
                self.head.prev = None 
        else: 
            curr = self.head   
            while curr: 
                if curr.value == value:
                    curr.prev.next = curr.next
                    # delete at tail 
                    if not curr.next:
                        self.tail = curr.prev 
                    else: 
                        curr.next.prev = curr.prev 
                    break       
                curr = curr.next
        self.length -= 1


    def find(self, value: int) -> DoubleNode:
        """
        Find a node with a specific value.
        """
        curr = self.head 
        while curr: 
            if curr.value == value: 
                return curr 
            curr = curr.next 
        return None 

    def size(self) -> int:
        """
        Returns the number of elements in the linked list.
        """
        return self.length 

    def is_empty(self) -> bool:
        """
        Checks if the linked list is empty.
        """
        return self.length == 0

    def print_list(self) -> None:
        """
        Prints all elements in the linked list.
        """
        curr = self.head 
        while curr: 
            print(curr.value)
            curr = curr.next


    def reverse(self) -> None:
        """
        Reverse the linked list in-place.
        """
        if not self.head or not self.head.next:
            return self.head

        prev = None 
        curr = self.head
        self.tail = self.head 
        while curr:
            prev = curr.prev
            curr.prev = curr.next
            curr.next = prev
            curr = curr.prev
        self.head = prev.prev


    def get_head(self) -> DoubleNode:
        """
        Returns the head node of the linked list.
        """
        return self.head 
    
    def get_tail(self) -> DoubleNode:
        """
        Returns the tail node of the linked list.
        """
        return self.tail 


class Queue:
    def __init__(self):
        """
        Initialize an empty queue.
        """
        self.size = 0 
        self.head = None 
        self.tail = None 

    def enqueue(self, value: int) -> None:
        """
        Add a value to the end of the queue.
        """
        node = DoubleNode(value) 
        if not self.head:
            self.head = node 
            self.tail = self.head 
        else: 
            self.tail.next = node 
            node.prev = self.tail 
            self.tail = node 
        self.size += 1


    def dequeue(self) -> int:
        """
        Remove a value from the front of the queue and return it.
        """
        if self.size == 0: 
            raise IndexError("Cannot remove from an empty queue.") 
        
        res = self.head.value 
        if self.size == 1: 
            self.head = None 
            self.tail = None 
        else: 
            self.head = self.head.next
            self.head.prev = None  
        self.size -= 1 
        return res 
    

    def peek(self) -> int:
        """
        Peek at the value at the front of the queue without removing it.
        """
        if self.size == 0: 
            raise IndexError("The queue is empty.")
        return self.head.value 
    

    def is_empty(self) -> bool:
        """
        Check if the queue is empty.
        """
        return self.size == 0  



class TreeNode:
    def __init__(self, value: int):
        """
        Initialize a tree node with value.
        """
        self.value = value  
        self.left = None 
        self.right = None 

class BinarySearchTree:
    def __init__(self):
        """
        Initialize an empty binary search tree.
        """
        self.root = None 
        self._size = 0 
        self._height = 0 
        self.min = TreeNode(float('inf'))
        self.max = TreeNode(-float('inf'))

    def insert(self, value: int) -> None:
        """
        Insert a node with a specific value into the binary search tree.
        """
        node = TreeNode(value)
        curr_height = 1 
        if not self.root: 
            self.root = node 
            self._height = 1
        else: 
            curr = self.root 
            while curr: 
                if curr.value < value: 
                    if not curr.right: 
                        curr.right = node
                        curr_height += 1
                        break 
                    curr = curr.right 
                else: 
                    if not curr.left: 
                        curr.left = node 
                        curr_height += 1
                        break 
                    curr = curr.left 
                curr_height += 1

        # update size 
        self._size += 1 
        # update height 
        self._height = max(self._height, curr_height)
        # update min 
        if node.value < self.min.value: 
            self.min = node 
        # update max 
        if node.value > self.max.value: 
            self.max = node


    def delete(self, value: int) -> None:
        """
        Remove a node with a specific value from the binary search tree.
        """

        def dfs(root, key): 
            if not root: 
                return 
            
            if root.value < key: 
                root.right = dfs(root.right, key)
            elif root.value > key:  
                root.left = dfs(root.left, key)
            elif root.value == key: 
                if not root.left: 
                    return root.right
                if not root.right: 
                    return root.left
                if root.right and root.left:
                    temp = root.right
                    while temp.left: 
                        temp = temp.left 
                    root.value = temp.val 
                    root.right= dfs(root.right, root.value)    
            return root
            
        def update_height(root):
            if not root: 
                return 0 
            l = update_height(root.left)
            r = update_height(root.right)
            return 1 + max(l,r)

        self.root = dfs(self.root, value)
        # update size
        self._size -= 1 
        # update height
        self._height = max(self._height, update_height(self.root))

        # update min 
        curr = self.root 
        while curr and curr.left: 
            curr = curr.left 
        self.min = curr

        # update max 
        curr = self.root 
        while curr and curr.right: 
            curr = curr.right 
        self.max = curr 


    def search(self, value: int) -> TreeNode:
        """
        Search for a node with a specific value in the binary search tree.
        """ 
        if not self.root: 
            return self.root 
        
        curr = self.root
        while curr: 
            if curr.value == value: 
                return curr 
            elif curr.value < value: 
                curr = curr.right 
            else: 
                curr = curr.left 
        return curr 


    def inorder_traversal(self) -> List[int]:
        """
        Perform an in-order traversal of the binary search tree.
        """
        stack = []
        ans = []
        curr = self.root 
        while stack or curr: 
            while curr:
                stack.append(curr)
                curr = curr.left 
            curr = stack.pop()
            ans.append(curr.value)
            curr = curr.right 
        return ans 
    
    def size(self) -> int:
        """
        Returns the number of nodes in the tree.
        """
        return self._size

    def is_empty(self) -> bool:
        """
        Checks if the tree is empty.
        """
        return self._size == 0 

    def height(self) -> int:
        """
        Returns the height of the tree.
        """
        return self._height

    def preorder_traversal(self) -> List[int]:
        """
        Perform a pre-order traversal of the tree.
        """
        stack = []
        ans = []
        curr = self.root 
        while stack or curr: 
            while curr:
                stack.append(curr)
                ans.append(curr.value)
                curr = curr.left 
            curr = stack.pop()
            curr = curr.right 
        return ans 

    def postorder_traversal(self) -> List[int]:
        """
        Perform a post-order traversal of the tree.
        """

        def dfs(root, res): 
            if not root: 
                return res 
            
            dfs(root.left, res)
            dfs(root.right, res)
            res.append(root.value)
            return res 
        
        ans = dfs(self.root, [])
        return ans 


    def level_order_traversal(self) -> List[int]:
        """
        Perform a level order (breadth-first) traversal of the tree.
        """
        import collections 
        def bfs(root): 
            q = collections.deque([root])
            ans = []

            while q: 
                node = q.popleft()
                ans.append(node.value)
                if node.left: 
                    q.append(node.left)
                if node.right: 
                    q.append(node.right)
            return ans 
        
        return bfs(self.root)


    def minimum(self) -> TreeNode:
        """
        Returns the node with the minimum value in the tree.
        """
        if not self.root: 
            raise ValueError("The tree is empty.")
        return self.min 

    def maximum(self) -> TreeNode:
        """
        Returns the node with the maximum value in the tree.
        """
        if not self.root: 
            raise ValueError("The tree is empty.")
        return self.max 
    

    def is_valid_bst(self) -> bool:
        """
        Check if the tree is a valid binary search tree.
        """
        def dfs(root, lo, hi): 
            if not root: 
                return True 
            if root.value <= lo or root.value>= hi: 
                return False 
            l = dfs(root.left, lo, root.value)
            r = dfs(root.right, root.value, hi) 
            return l and r 
        
        return dfs(self.root, -float('inf'), float('inf'))



def insertion_sort(lst: List[int]) -> List[int]:
    def swap(arr, i, j): 
        arr[i], arr[j] = arr[j], arr[i]

    if not lst: 
        return lst 
    
    for i in range(1, len(lst)): 
        j = i 
        while (j > 0 and lst[j-1] > lst[j]): 
            swap(lst, j-1, j)
            j -= 1
    return lst 
    

def selection_sort(lst: List[int]) -> List[int]:
    def swap(arr, i, j): 
        arr[i], arr[j] = arr[j], arr[i]

    if not lst: 
        return lst 

    n = len(lst)
    for i in range(n): 
        swap_index = i 
        for j in range(i+1, n): 
            if lst[j] < lst[swap_index]: 
                swap_index = j 
        swap(lst, i, swap_index)
    return lst 
     

def bubble_sort(lst: List[int]) -> List[int]:
    def swap(arr, i, j): 
        arr[i], arr[j] = arr[j], arr[i]

    if not lst: 
        return lst 

    n = len(lst)
    for _ in range(n):
        flag = True  
        for j in range(n-1):
            if lst[j+1] < lst[j]: 
                swap(lst, j, j+1)
                flag = False 
        if flag: 
            return lst 
    return lst 


def shell_sort(lst: List[int]) -> List[int]:
    gap = len(lst)//2
    while gap > 0:
        for i in range(0,len(lst)-gap):
            for j in range(i+gap,len(lst),gap):
                temp = lst[j]
                while j-gap>=i and temp < lst[j-gap]:
                    lst[j] = lst[j-gap]
                    j -= gap
                lst[j] = temp
        gap = gap//2
    return lst 


def merge_sort(lst: List[int]) -> List[int]:
    if len(lst) <= 1: 
        return lst 
    mid = len(lst) // 2
    left = merge_sort(lst[:mid])
    right = merge_sort(lst[mid:])
    return merge(left, right)

def merge(left, right): 
    if not left: 
        return right 
    if not right: 
        return left 
    
    res = []
    m,n = len(left), len(right)
    i,j = 0, 0 
    while i < m and j < n: 
        if left[i] <= right[j]: 
            res.append(left[i])
            i += 1 
        else: 
            res.append(right[j])
            j += 1
    if left: 
        res.extend(left[i:])
    if right: 
        res.extend(right[j:])
    return res 



def quick_sort(lst: List[int]) -> List[int]:

    def quicksort(arr, left, right): 
        if left < right: 
            pos = partition(arr, left, right)
            quicksort(arr, left, pos-1)
            quicksort(arr, pos+1, right)
    
    def partition(arr, left, right): 
        i = left
        j = right-1
        pivot = arr[right]

        while i < j: 
            while i < right and arr[i] < pivot: 
                i += 1 
            while j > left and arr[j] >= pivot: 
                j -= 1
            if i < j: 
                arr[i], arr[j] = arr[j], arr[i]
        if arr[i] > pivot: 
            arr[i], arr[right] = arr[right], arr[i]
        return i 
    
    quicksort(lst, 0, len(lst)-1)
    return lst 
    
