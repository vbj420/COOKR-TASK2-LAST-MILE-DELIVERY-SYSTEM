import tkinter as tk
from tkinter import messagebox
import csv
import os

class OrderPrompt:
    def __init__(self, root, customer_name, customer_location):
        self.root = root
        self.queue = []
        self.customer_name = customer_name
        self.customer_location = customer_location
        self.current_order = None
        self.create_order_window()

    def create_order_window(self):
        if self.queue:
            self.current_order = self.queue.pop(0)
            self.order_window = tk.Toplevel(self.root)
            self.order_window.title(f"Order {self.current_order['order_number']}")

            food_label = tk.Label(self.order_window, text=f"Food name for order {self.current_order['order_number']}:")
            food_label.pack()
            self.food_entry = tk.Entry(self.order_window)
            self.food_entry.pack()

            kitchen_label = tk.Label(self.order_window, text=f"Kitchen ID for order {self.current_order['order_number']}:")
            kitchen_label.pack()
            self.kitchen_entry = tk.Entry(self.order_window)
            self.kitchen_entry.pack()

            delivery_label = tk.Label(self.order_window, text=f"Delivery time for order {self.current_order['order_number']}:")
            delivery_label.pack()
            self.delivery_entry = tk.Entry(self.order_window)
            self.delivery_entry.pack()

            save_button = tk.Button(self.order_window, text="Save", command=self.save_and_calculate_distance)
            save_button.pack()
        else:
            messagebox.showinfo("Success", "All orders have been processed.")

    def save_and_calculate_distance(self):
        food_name = self.food_entry.get()
        kitchen_id = self.kitchen_entry.get()
        delivery_time = self.delivery_entry.get()

        kitchen_location = self.get_kitchen_location(kitchen_id)
        if kitchen_location:
            distance_from_kitchen = self.calculate_distance(kitchen_location)
            self.write_order_to_csv(food_name, kitchen_id, delivery_time, distance_from_kitchen)
            self.order_window.destroy()
            self.create_order_window()
        else:
            messagebox.showerror("Error", f"Kitchen ID {kitchen_id} not found.")

    def get_kitchen_location(self, kitchen_id):
        with open('Kitchens.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == kitchen_id:
                    return float(row[1]), float(row[2])  # Assuming the kitchen coordinates are in the second and third columns
        return None

    def calculate_distance(self, kitchen_location):
        distance = ((self.customer_location[0] - kitchen_location[0]) ** 2 + (self.customer_location[1] - kitchen_location[1]) ** 2) ** 0.5
        return round(distance, 2)

    def write_order_to_csv(self, food_name, kitchen_id, delivery_time, distance_from_kitchen):
        # Check if the Orders.csv file exists
        if not os.path.exists('Orders.csv'):
            with open('Orders.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Customer Name', 'Customer Location X', 'Customer Location Y', 'Kitchen ID', 'Kitchen Location X', 'Kitchen Location Y', 'Food Name', 'Delivery Time', 'Distance from Kitchen'])
        
        # Get kitchen location
        kitchen_location = self.get_kitchen_location(kitchen_id)
        if kitchen_location:
            with open('Orders.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([self.customer_name, self.customer_location[0], self.customer_location[1], kitchen_id, kitchen_location[0], kitchen_location[1], food_name, delivery_time, distance_from_kitchen])
        else:
            messagebox.showerror("Error", f"Kitchen ID {kitchen_id} not found.")

def save_order():
    customer_name = name_entry.get()
    customer_location = (float(x_entry.get()), float(y_entry.get()))
    num_orders = int(orders_entry.get())

    order_prompt = OrderPrompt(root, customer_name, customer_location)

    for i in range(num_orders):
        order = {'order_number': i + 1}
        order_prompt.queue.append(order)
    order_prompt.create_order_window()

root = tk.Tk()
root.title("Order Entry")

name_label = tk.Label(root, text="Customer Name:")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()

x_label = tk.Label(root, text="Customer Location X:")
x_label.pack()
x_entry = tk.Entry(root)
x_entry.pack()

y_label = tk.Label(root, text="Customer Location Y:")
y_label.pack()
y_entry = tk.Entry(root)
y_entry.pack()

orders_label = tk.Label(root, text="Number of Orders:")
orders_label.pack()
orders_entry = tk.Entry(root)
orders_entry.pack()

submit_button = tk.Button(root, text="Submit", command=save_order)
submit_button.pack()

root.mainloop()
