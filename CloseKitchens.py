import math
import csv

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

# Print unique kitchen pairs with distance <= 10
printed_pairs = set()
for k1, (x1, y1) in kitchens.items():
    for k2, (x2, y2) in kitchens.items():
        if k1 != k2 and ((k1, k2) not in printed_pairs) and ((k2, k1) not in printed_pairs):
            dist = distance((x1, y1), (x2, y2))
            if dist <= 10:
                printed_pairs.add((k1, k2))
                print(f"Kitchen pair ({k1}, {k2}) - Distance: {dist}")
