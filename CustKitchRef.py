import math
import csv
import tkinter as tk

# Define a function to calculate the distance between two points
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Read kitchen coordinates from the file Kitchens.csv
kitchens = {}
with open('Kitchens.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        kitchen, x, y = row
        kitchens[kitchen] = (int(x), int(y))

# Function to find top 10 closest kitchens to the customer
def find_closest_kitchens(customer_x, customer_y):
    distances = []
    for kitchen, (x, y) in kitchens.items():
        dist = distance((customer_x, customer_y), (x, y))
        distances.append((kitchen, dist))
    distances.sort(key=lambda x: x[1])  # Sort based on distance
    return distances[:10]  # Return top 10 closest kitchens

# Function to display the top 10 closest kitchens on a Tkinter screen
def display_closest_kitchens():
    customer_name = entry_name.get()
    customer_x = int(entry_x.get())
    customer_y = int(entry_y.get())

    closest_kitchens = find_closest_kitchens(customer_x, customer_y)

    # Display top 10 closest kitchens on the Tkinter screen
    for i, (kitchen, dist) in enumerate(closest_kitchens):
        label = tk.Label(root, text=f"{i+1}. {kitchen} - Distance: {dist}")
        label.pack()

# Create a Tkinter window
root = tk.Tk()
root.title("Top 10 Closest Kitchens")

# Customer input fields
tk.Label(root, text="Customer Name:").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Customer X Coordinate:").pack()
entry_x = tk.Entry(root)
entry_x.pack()

tk.Label(root, text="Customer Y Coordinate:").pack()
entry_y = tk.Entry(root)
entry_y.pack()

# Button to find closest kitchens
find_button = tk.Button(root, text="Find Closest Kitchens", command=display_closest_kitchens)
find_button.pack()

# Run the Tkinter event loop
root.mainloop()
