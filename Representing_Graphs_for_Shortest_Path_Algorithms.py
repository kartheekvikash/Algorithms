#code by Kartheek Vikash Meesala
#email: letter2kartheekvikashmeesala@gmail.com
#Run it in VScode or Jupitor as online compilers may not support GUI output
#https://github.com/kartheekvikash/Algorithms.git


import tkinter as tk  # Import the Tkinter module for GUI creation
import math  # Import math module to represent infinity

class GraphApp:
    def __init__(self, root):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("Graph Representation (Adjacency Matrix)")  # Set window title
        self.root.geometry("1200x700")  # Increase GUI size to fit screen

        self.vertices = []  # List to store user-entered vertices
        self.edges = {}  # Dictionary to store graph edges with weights

        # Labels and Entry Fields for User Input
        tk.Label(root, text="Enter Vertices (Comma-separated):", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=10)
        self.vertices_entry = tk.Entry(root, font=("Arial", 12), width=40)  # Entry field for vertices
        self.vertices_entry.grid(row=0, column=1, padx=10)

        tk.Label(root, text="Enter Edge (Example: A B 2):", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=10)
        self.edge_entry = tk.Entry(root, font=("Arial", 12), width=40)  # Entry field for edges
        self.edge_entry.grid(row=1, column=1, padx=10)

        # Buttons to interact with the application
        tk.Button(root, text="Set Vertices", font=("Arial", 12), command=self.set_vertices, width=15).grid(row=0, column=2, padx=10)
        tk.Button(root, text="Add Edge", font=("Arial", 12), command=self.add_edge, width=15).grid(row=1, column=2, padx=10)
        tk.Button(root, text="Generate Matrix", font=("Arial", 12), command=self.display_matrix, width=15).grid(row=2, column=1, padx=10)
        tk.Button(root, text="Clear Output", font=("Arial", 12), command=self.clear_output, width=15).grid(row=3, column=2, padx=10)  # New button to clear output

        # Output Text Box to display results
        self.output_box = tk.Text(root, height=30, width=120, font=("Arial", 12))
        self.output_box.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    def set_vertices(self):
        """Extract and store vertices from user input."""
        self.vertices = self.vertices_entry.get().split(",")  # Split input by commas
        self.vertices = [v.strip() for v in self.vertices]  # Remove extra spaces
        self.output_box.insert(tk.END, f"Vertices set: {', '.join(self.vertices)}\n")

    def add_edge(self):
        """Extract and store edges with weights from user input."""
        data = self.edge_entry.get().split()  # Get user input and split it into components

        if len(data) != 3:  # Ensure the format is correct
            self.output_box.insert(tk.END, "Invalid format! Use: A B 2\n")
            return

        u, v, w = data  # Extract vertices and edge weight
        try:
            weight = int(w)  # Convert weight to integer
            if u in self.vertices and v in self.vertices:  # Ensure vertices exist in the graph
                self.edges[(u, v)] = weight  # Store the edge in the dictionary
                self.output_box.insert(tk.END, f"Added Edge: {u} → {v} = {weight}\n")
            else:
                self.output_box.insert(tk.END, "Invalid vertices! Make sure they exist.\n")
        except ValueError:
            self.output_box.insert(tk.END, "Weight must be an integer!\n")  # Error handling for invalid weight input

    def clear_output(self):
        """Clears the output box for new inputs."""
        self.output_box.delete("1.0", tk.END)  # Deletes all text inside the output box

    def display_matrix(self):
        """Generates and displays the adjacency matrix."""
        num_vertices = len(self.vertices)  # Get the number of vertices
        adj_matrix = [[math.inf] * num_vertices for _ in range(num_vertices)]  # Initialize matrix with infinity

        # Set diagonal entries to 0 (self-distance)
        for i in range(num_vertices):
            adj_matrix[i][i] = 0  

        # Populate the adjacency matrix with weights
        for (u, v), weight in self.edges.items():
            i, j = self.vertices.index(u), self.vertices.index(v)  # Get indices for vertices
            adj_matrix[i][j] = weight  # Set edge weight in the matrix

        # Explanation of how the adjacency matrix works
        explanation = """
        📌 Algorithm Used: Graph Representation & Adjacency Matrix

        1️⃣ The user enters multiple vertices.
        2️⃣ Edges and weights are dynamically added between vertices.
        3️⃣ An adjacency matrix is generated where:
            - If an edge exists, its weight is inserted.
            - If there's no direct connection, it's marked as ∞ (infinity).
            - Diagonal entries are set to 0 (self-distance).

        Example Input:
        - Vertices: A, B, C, D
        - Edges: A → B = 3, B → C = 5, C → D = 2

        Expected Output (Adjacency Matrix):
        [0, 3, ∞, ∞]
        [∞, 0, 5, ∞]
        [∞, ∞, 0, 2]
        [∞, ∞, ∞, 0]

        This method is commonly used in shortest path algorithms like Dijkstra and Bellman-Ford.
        """
        self.output_box.insert(tk.END, "\n" + explanation + "\nAdjacency Matrix (∞ represents missing edges):\n")
        
        # Display the final adjacency matrix in GUI output
        for row in adj_matrix:
            row_display = ["∞" if val == math.inf else val for val in row]  # Replace infinity with ∞ for display clarity
            self.output_box.insert(tk.END, str(row_display) + "\n")

# Run Tkinter App
root = tk.Tk()  # Initialize Tkinter
app = GraphApp(root)  # Create an instance of the GraphApp class
root.mainloop()  # Run the GUI loop