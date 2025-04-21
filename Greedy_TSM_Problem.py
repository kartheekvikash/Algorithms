import tkinter as tk
from tkinter import messagebox
import math

# Function to calculate distance between two points
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Greedy TSP algorithm
def greedy_tsp(points):
    visited = []
    total_distance = 0
    current_point = points.pop(0)
    visited.append(current_point)

    while points:
        # Find the closest point
        closest_point = min(points, key=lambda point: distance(current_point, point))
        total_distance += distance(current_point, closest_point)
        visited.append(closest_point)
        points.remove(closest_point)
        current_point = closest_point

    # Return to the starting point
    total_distance += distance(current_point, visited[0])
    visited.append(visited[0])

    return visited, total_distance

# Function to arrange points in a pyramid shape
def arrange_pyramid_points(points, canvas_width, canvas_height):
    pyramid_levels = len(points)
    arranged_points = []
    
    spacing_x = canvas_width // (pyramid_levels + 1)
    spacing_y = canvas_height // (pyramid_levels + 1)
    
    index = 0
    for level in range(1, pyramid_levels + 1):
        row_points = []
        for i in range(level):
            if index < len(points):
                x = spacing_x * (i + 1) + (canvas_width // 2 - level * spacing_x // 2)
                y = level * spacing_y
                row_points.append((x, y))
                index += 1
        arranged_points.extend(row_points)
    
    return arranged_points

# GUI setup for custom coordinates
def visualize_tsp():
    try:
        # Parse user-provided coordinates
        points = [
            tuple(map(int, coord.split(',')))
            for coord in entry_points.get().strip().split(';')
        ]
    except ValueError:
        messagebox.showerror("Error", "Invalid input format. Use 'x1,y1;x2,y2;...'")
        return

    # Arrange points in a pyramid structure
    arranged_points = arrange_pyramid_points(points, canvas_width=1000, canvas_height=800)

    # Perform TSP greedy algorithm
    visited, total_distance = greedy_tsp(arranged_points[:])  # Preserve original points

    # Visualize results
    canvas.delete("all")
    
    # Draw each point entered by the user
    for i, (x, y) in enumerate(arranged_points):
        canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")  # Display points in pyramid shape
        canvas.create_text(x, y - 10, text=f"P{i+1}", fill="black")  # Label each point
    
    # Draw the traveling salesman path
    for i in range(len(visited) - 1):
        x1, y1 = visited[i]
        x2, y2 = visited[i + 1]
        canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)

        # Highlight visited points along the path
        canvas.create_oval(x1-5, y1-5, x1+5, y1+5, fill="green")
        canvas.create_text(x1, y1 - 10, text=f"{i + 1}", fill="black")

    result_label.config(
        text=f"Total Distance: {total_distance:.2f}\nVisited Order: {visited}"
    )

# Create main window
root = tk.Tk()
root.title("Greedy TSP Solver with Pyramid Structure")
root.geometry("1200x800")  # Set the window size

# Input field for custom points
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Enter custom points (x1,y1;x2,y2;...):").pack(side=tk.LEFT, padx=5)
entry_points = tk.Entry(frame, width=40)
entry_points.pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Solve TSP", command=visualize_tsp).pack(side=tk.LEFT, padx=5)

# Expanded Canvas for visualization
canvas = tk.Canvas(root, width=1000, height=800, bg="white")
canvas.pack(pady=10)

# Label for result
result_label = tk.Label(root, text="Total Distance: N/A\nVisited Order: N/A", font=("Arial", 14))
result_label.pack(pady=10)

# Algorithm Definition & Uses
algo_label = tk.Label(root, text=(
    "Algorithm: Greedy Traveling Salesman Problem (TSP)\n\n"
    "Definition: The Greedy TSP algorithm finds an approximate shortest route "
    "by always selecting the closest next point. While not optimal, it provides "
    "a fast and efficient solution in many practical scenarios.\n\n"
    "Real-World Applications:\n"
    "• Delivery route optimization (e.g., postal services)\n"
    "• Circuit design for minimal wiring connections\n"
    "• Logistics planning for warehouse operations\n"
    "• City traffic routing for autonomous vehicles"
), font=("Arial", 12), justify="left", wraplength=1100)
algo_label.pack(pady=20)

root.mainloop()