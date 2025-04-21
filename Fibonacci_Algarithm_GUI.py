#code by Kartheek Vikash Meesala
#email: letter2kartheekvikashmeesala@gmail.com
#Run it in VScode or Jupitor as online compilers may not support GUI output
#https://github.com/kartheekvikash/Algorithms.git

import math
import tkinter as tk
from tkinter import messagebox

# Fibonacci Heap Node
class Node:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.mark = False
        self.next = self
        self.prev = self

# Fibonacci Heap Class
class FibonacciHeap:
    def __init__(self):
        self.min_node = None
        self.num_nodes = 0

    def insert(self, key):
        node = Node(key)
        if self.min_node is None:
            self.min_node = node
        else:
            self._add_to_root_list(node)
            if node.key < self.min_node.key:
                self.min_node = node
        self.num_nodes += 1

    def _add_to_root_list(self, node):
        node.next = self.min_node
        node.prev = self.min_node.prev
        self.min_node.prev.next = node
        self.min_node.prev = node

    def find_min(self):
        return self.min_node.key if self.min_node else None

    def extract_min(self):
        z = self.min_node
        if z:
            if z.child:
                children = []
                child = z.child
                while True:
                    children.append(child)
                    child = child.next
                    if child == z.child:
                        break
                for child in children:
                    self._add_to_root_list(child)
                    child.parent = None
            
            z.prev.next = z.next
            z.next.prev = z.prev

            if z == z.next:
                self.min_node = None
            else:
                self.min_node = z.next
                self._consolidate()
            self.num_nodes -= 1
        return z.key if z else None

    def _consolidate(self):
        A = [None] * (int(math.log(self.num_nodes) * 2) + 1)
        nodes = []
        x = self.min_node
        while True:
            nodes.append(x)
            x = x.next
            if x == self.min_node:
                break
        for w in nodes:
            x = w
            d = x.degree
            while A[d]:
                y = A[d]
                if x.key > y.key:
                    x, y = y, x
                self._link(y, x)
                A[d] = None
                d += 1
            A[d] = x
        
        self.min_node = None
        for i in range(len(A)):
            if A[i]:
                if not self.min_node or A[i].key < self.min_node.key:
                    self.min_node = A[i]

    def _link(self, y, x):
        y.prev.next = y.next
        y.next.prev = y.prev
        y.parent = x
        y.next = y
        y.prev = y
        if not x.child:
            x.child = y
        else:
            y.next = x.child
            y.prev = x.child.prev
            x.child.prev.next = y
            x.child.prev = y
        x.degree += 1
        y.mark = False

# GUI functions
def insert_values():
    try:
        values = list(map(int, entry.get().split(',')))  # Allow multiple inputs separated by commas
        for value in values:
            fib_heap.insert(value)
        update_display()
    except ValueError:
        messagebox.showerror("Error", "Invalid input! Enter numeric values separated by commas.")

def extract_minimum():
    extracted = fib_heap.extract_min()
    if extracted is not None:
        messagebox.showinfo("Extracted Minimum", f"Extracted Minimum: {extracted}")
        update_display()
    else:
        messagebox.showerror("Error", "Heap is empty!")

def update_display():
    min_value = fib_heap.find_min()
    min_label.config(text=f"Minimum Element: {min_value if min_value is not None else 'N/A'}")

# GUI Setup
fib_heap = FibonacciHeap()
root = tk.Tk()
root.title("Fibonacci Heap GUI")
root.geometry("500x400")

# Input frame
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Enter values (comma-separated):").pack(side=tk.LEFT, padx=5)
entry = tk.Entry(frame, width=20)
entry.pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Insert", command=insert_values).pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Extract Min", command=extract_minimum).pack(side=tk.LEFT, padx=5)

# Display the minimum element
min_label = tk.Label(root, text="Minimum Element: N/A", font=("Arial", 14))
min_label.pack(pady=10)

# Algorithm definition and real-time applications
algo_label = tk.Label(root, text=(
    "Algorithm: Fibonacci Heap\n\n"
    "Definition: A data structure optimized for fast priority queue operations, allowing \n"
    "efficient insertions, deletions, and minimum extractions with amortized logarithmic complexity.\n\n"
    "Real-World Applications:\n"
    "• **Real-time scheduling** (OS process management)\n"
    "• **Graph algorithms** (Dijkstra's shortest path, Prim's MST)\n"
    "• **Cache management** (efficient priority-based access)\n"
    "• **AI and robotics** (decision-making under time constraints)"
), font=("Arial", 12), justify="left", wraplength=450)
algo_label.pack(pady=20)

root.mainloop()
