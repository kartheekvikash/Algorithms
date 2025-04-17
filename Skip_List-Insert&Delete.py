#code by Kartheek Vikash Meesala
#email: letter2kartheekvikashmeesala@gmail.com
#Run it in VScode or Jupitor as online compilers may not support GUI output
#https://github.com/kartheekvikash/Algorithms.git


import tkinter as tk  # Import tkinter for GUI creation
from tkinter import messagebox, scrolledtext  # Import messagebox for alerts, scrolledtext for large text fields
import random  # Import random module for probabilistic level assignment

# ---------------------------- Skip List Node Definition ---------------------------- #

class Node:
    """Represents a node in the Skip List."""
    def __init__(self, key, level):
        self.key = key  # Stores the key (value) of the node
        self.forward = [None] * (level + 1)  # Pointers to next nodes at different levels

# ---------------------------- Skip List Data Structure ---------------------------- #

class SkipList:
    """Skip List data structure supporting insert, search, and delete operations."""
    def __init__(self, max_level, p):
        """
        Initializes the Skip List.
        :param max_level: Maximum level allowed in the Skip List.
        :param p: Probability factor for level increment.
        """
        self.max_level = max_level  # Maximum levels allowed
        self.p = p  # Probability for determining node levels
        self.header = Node(None, max_level)  # Header (sentinel) node with max levels
        self.level = 0  # Current highest level in the list

    def random_level(self):
        """
        Generates a random level for a new node based on probability 'p'.
        Higher probability results in taller levels.
        """
        lvl = 0
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def insert(self, key):
        """
        Inserts a key into the Skip List.
        - Determines the level for the new node using `random_level()`.
        - Updates forward pointers to maintain structure.
        """
        update = [None] * (self.max_level + 1)  # Tracks nodes that need updating
        current = self.header  # Start from header node
        
        # Move through levels from highest to lowest
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current  # Store reference for level updates

        level = self.random_level()  # Determine the level for the new node
        if level > self.level:  # If new level is higher, update header references
            for i in range(self.level + 1, level + 1):
                update[i] = self.header
            self.level = level  # Update Skip List level

        new_node = Node(key, level)  # Create new node with assigned level
        for i in range(level + 1):  # Link the new node at each level
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def delete(self, key):
        """
        Deletes a key from the Skip List.
        - Updates pointers to skip the deleted node.
        - Reduces the list height if necessary.
        """
        update = [None] * (self.max_level + 1)
        current = self.header
        
        # Find the key location in all levels
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current  # Store nodes that need updates

        current = current.forward[0]  # Move to next node at base level
        if current and current.key == key:  # Key found
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]

            # Reduce the level if highest-level nodes are removed
            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1

    def display(self):
        """
        Returns a formatted representation of the Skip List with levels.
        Shows how elements are connected at each level.
        """
        levels = [[] for _ in range(self.level + 1)]
        current = self.header.forward[0]

        while current:
            for i in range(len(current.forward)):
                levels[i].append(current.key)
            current = current.forward[0]

        output = "**Skip List Structure:**\n"
        for i in range(self.level, -1, -1):  # Show levels from highest to lowest
            output += f"Level {i}: " + " -> ".join(map(str, levels[i])) + " -> None\n"
        return output.strip()

# ---------------------------- GUI Implementation ---------------------------- #

class SkipListGUI:
    """Handles GUI interactions for the Skip List."""
    def __init__(self, root):
        self.skip_list = SkipList(max_level=4, p=0.5)  # Create Skip List with max levels
        root.title("Skip List GUI")  # Set window title
        root.geometry("1200x800")  # Enlarged window size for better visualization

        # User input for adding numbers
        tk.Label(root, text="Enter Numbers (comma separated):").pack()
        self.num_entry = tk.Entry(root, width=50)
        self.num_entry.pack()
        tk.Button(root, text="Add Numbers", command=self.add_numbers).pack()

        # Insert new number
        tk.Label(root, text="Insert Number:").pack()
        self.insert_entry = tk.Entry(root, width=50)
        self.insert_entry.pack()
        tk.Button(root, text="Insert", command=self.insert_number).pack()

        # Delete number
        tk.Label(root, text="Delete Number:").pack()
        self.delete_entry = tk.Entry(root, width=50)
        self.delete_entry.pack()
        tk.Button(root, text="Delete", command=self.delete_number).pack()

        # Display area for Skip List structure
        self.display_text = scrolledtext.ScrolledText(root, width=120, height=20, wrap=tk.WORD)
        self.display_text.pack()
        tk.Button(root, text="Show Skip List", command=self.display_list).pack()

        # Algorithm description area
        self.description_text = scrolledtext.ScrolledText(root, width=120, height=10, wrap=tk.WORD)
        self.description_text.pack()
        self.display_algorithm_description()

    def display_algorithm_description(self):
        """Displays algorithm details in the GUI."""
        description = (
            "**Skip List Algorithm:**\n"
            "A Skip List is a probabilistic data structure that allows fast searching, "
            "insertion, and deletion by using multiple levels of linked nodes.\n\n"
            "**How It Works:**\n"
            "✔ Each node has links to multiple levels\n"
            "✔ Higher-level pointers allow fast skipping over elements\n"
            "✔ Probability 'p' determines how levels are assigned\n\n"
            "**Operations:**\n"
            "🔹 Search: Moves across levels for fast lookup\n"
            "🔹 Insert: Places element at a random level and connects it\n"
            "🔹 Delete: Removes references from all levels\n\n"
            "**Uses of Skip List:**\n"
            "✔ Database indexing\n"
            "✔ Network routing tables\n"
            "✔ Memory-efficient alternative to balanced trees\n"
            "✔ Helps in implementing priority queues efficiently"
        )
        self.description_text.insert(tk.END, description)

    # Functions for adding, inserting, and deleting numbers in the Skip List
    def add_numbers(self):
        numbers = self.num_entry.get().split(",")
        try:
            numbers = [int(num.strip()) for num in numbers]
            for num in numbers:
                self.skip_list.insert(num)
            self.display_list()
        except ValueError:
            messagebox.showerror("Error", "Enter valid numbers!")

    def insert_number(self):
        num = int(self.insert_entry.get())
        self.skip_list.insert(num)
        self.display_list()

    def delete_number(self):
        num = int(self.delete_entry.get())
        self.skip_list.delete(num)
        self.display_list()

    def display_list(self):
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, self.skip_list.display())

root = tk.Tk()
app = SkipListGUI(root)
root.mainloop()