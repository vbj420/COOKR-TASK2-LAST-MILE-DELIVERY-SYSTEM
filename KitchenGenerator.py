# generate kitchens
# geo-spatial data
# there are 40 kitchens in the city 
import csv
import random
# Define the range of the city
x_range = range(0, 201)
y_range = range(0, 201)
# Generate 30 random kitchen coordinates
kitchens = {}
for i in range(1, 41):
    x = random.choice(x_range)
    y = random.choice(y_range)
    kitchens[f'k{i}'] = (x, y)
# Write the kitchens dictionary to a CSV file
with open('Kitchens.csv', 'w', newline='') as csvfile:
    fieldnames = ['Kitchen', 'X', 'Y']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for kitchen, (x, y) in kitchens.items():
        writer.writerow({'Kitchen': kitchen, 'X': x, 'Y': y})

print("Data written to kitchens.csv")
