#code by Kartheek Vikash Meesala
#email: letter2kartheekvikashmeesala@gmail.com
#Run it in VScode or Jupitor as online compilers may not support GUI output
#https://github.com/kartheekvikash/Algorithms.git


import tkinter as tk  # Import the Tkinter library for GUI creation
import math  # Import math module to use infinity representation

class BellmanFordApp:
    """GUI-based application for implementing the Bellman-Ford algorithm."""
    
    def __init__(self, root):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("Bellman-Ford Algorithm (GUI)")  # Set window title
        self.root.geometry("1200x700")  # Set full-screen size for better readability

        self.vertices = []  # List to store vertices entered by the user
        self.edges = []  # List to store edges along with weights

        # Labels and input fields for user interaction
        tk.Label(root, text="Enter Vertices (Comma-separated):", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=10)
        self.vertices_entry = tk.Entry(root, font=("Arial", 12), width=40)  # Input field for vertices
        self.vertices_entry.grid(row=0, column=1, padx=10)

        tk.Label(root, text="Enter Edge (Example: A B -2):", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=10)
        self.edge_entry = tk.Entry(root, font=("Arial", 12), width=40)  # Input field for edges
        self.edge_entry.grid(row=1, column=1, padx=10)

        tk.Label(root, text="Select Source Vertex:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=10)
        self.source_entry = tk.Entry(root, font=("Arial", 12), width=40)  # Input field for source vertex
        self.source_entry.grid(row=2, column=1, padx=10)

        # Buttons for user actions
        tk.Button(root, text="Set Vertices", font=("Arial", 12), command=self.set_vertices, width=15).grid(row=0, column=2, padx=10)
        tk.Button(root, text="Add Edge", font=("Arial", 12), command=self.add_edge, width=15).grid(row=1, column=2, padx=10)
        tk.Button(root, text="Run Bellman-Ford", font=("Arial", 12), command=self.run_bellman_ford, width=15).grid(row=2, column=2, padx=10)
        tk.Button(root, text="Clear Output", font=("Arial", 12), command=self.clear_output, width=15).grid(row=3, column=2, padx=10)  # Button to clear output

        # Output text box to display results
        self.output_box = tk.Text(root, height=30, width=120, font=("Arial", 12))  # Text box for output display
        self.output_box.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    def set_vertices(self):
        """Extract and store vertices from user input."""
        self.vertices = self.vertices_entry.get().split(",")  # Split input string by commas
        self.vertices = [v.strip() for v in self.vertices]  # Remove extra spaces around vertices
        self.output_box.insert(tk.END, f"Vertices set: {', '.join(self.vertices)}\n")  # Display confirmation in output

    def add_edge(self):
        """Extract and store edges with weights from user input."""
        data = self.edge_entry.get().split()  # Get user input and split it into components

        if len(data) != 3:  # Ensure correct format
            self.output_box.insert(tk.END, "Invalid format! Use: A B -2\n")  # Display error message
            return

        u, v, w = data  # Extract vertices and weight
        try:
            weight = int(w)  # Convert weight to integer
            if u in self.vertices and v in self.vertices:  # Ensure vertices exist
                self.edges.append((u, v, weight))  # Store edge in list
                self.output_box.insert(tk.END, f"Added Edge: {u} → {v} = {weight}\n")  # Confirm addition
            else:
                self.output_box.insert(tk.END, "Invalid vertices! Make sure they exist.\n")  # Error message for non-existent vertices
        except ValueError:
            self.output_box.insert(tk.END, "Weight must be an integer!\n")  # Error message for invalid weight input

    def clear_output(self):
        """Clears the output box for new inputs."""
        self.output_box.delete("1.0", tk.END)  # Clears all output text

    def run_bellman_ford(self):
        """Executes the Bellman-Ford algorithm and displays results."""
        source = self.source_entry.get().strip()  # Get source vertex from user input
        if source not in self.vertices:  # Validate source vertex
            self.output_box.insert(tk.END, "Invalid source vertex!\n")  # Error message
            return

        num_vertices = len(self.vertices)  # Get number of vertices
        distance = {vertex: math.inf for vertex in self.vertices}  # Initialize distances with infinity
        distance[source] = 0  # Set source vertex distance to 0

        # Execute Bellman-Ford Algorithm
        self.output_box.insert(tk.END, "\nStep-by-step Bellman-Ford execution:\n")
        for _ in range(num_vertices - 1):  # Iterate |V| - 1 times
            for u, v, weight in self.edges:  # Traverse all edges
                if distance[u] != math.inf and distance[u] + weight < distance[v]:  # Relaxation condition
                    distance[v] = distance[u] + weight  # Update distance
                    self.output_box.insert(tk.END, f"Updated Distance: {u} → {v}, New Cost: {distance[v]}\n")  # Display update

        # Detect negative-weight cycles
        for u, v, weight in self.edges:
            if distance[u] != math.inf and distance[u] + weight < distance[v]:  # If relaxation still occurs
                self.output_box.insert(tk.END, "\n⚠️ Graph contains a negative weight cycle!\n")  # Display cycle warning
                return

        # Display final shortest paths
        self.output_box.insert(tk.END, "\n🔹 Final Shortest Paths from Source:\n")
        for vertex in self.vertices:
            if distance[vertex] == math.inf:
                self.output_box.insert(tk.END, f"{source} → {vertex}: ∞ (No Path)\n")  # No valid path
            else:
                self.output_box.insert(tk.END, f"{source} → {vertex}: {distance[vertex]}\n")  # Display shortest path result

        # Bellman-Ford Algorithm Explanation
        bellman_ford_explanation = f"""
        📌 What is Bellman-Ford Algorithm?
        - The Bellman-Ford Algorithm is a **graph-based shortest path algorithm** that finds the shortest distances from a single source to all other vertices.
        - It works well for **graphs with negative weights** and can detect **negative-weight cycles**.

        🔹 How does it work?
        1️⃣ Initializes all distances to **infinity (∞)** except the source, which is set to **0**.
        2️⃣ Iterates through all edges **|V| - 1 times** to relax them.
        3️⃣ If an edge can still reduce a distance after all iterations, it means a **negative cycle exists**.
        4️⃣ Finally, it returns the shortest paths from the source vertex.

        💡 How It Worked for Inserted Values:
        - **Source Vertex:** {source}
        - Processed **{len(self.edges)} edges** to update shortest paths.
        - Displayed **valid shortest paths** and detected any **negative cycles**.

        🎯 Try different graphs and observe how Bellman-Ford finds optimal paths!
        """
        self.output_box.insert(tk.END, bellman_ford_explanation)  # Add explanation to output

# Run Tkinter App
root = tk.Tk()  # Initialize Tkinter
app = BellmanFordApp(root)  # Create an instance of the BellmanFordApp class
root.mainloop()  # Run the GUI loop